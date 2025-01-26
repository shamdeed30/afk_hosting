import cv2 as cv
import numpy as np
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


#Load screenshot
for i in range(8):
    players = {}
    img_rgb = cv.imread(f'Valorant/Scoreboards/{i}.png')

    img_rgb = cv.resize(img_rgb, (1920, 1080))
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)

    img_map = img_gray[100:150, 60:240]
    img_map = cv.adaptiveThreshold(
        img_map, 
        255,
        cv.ADAPTIVE_THRESH_MEAN_C, 
        cv.THRESH_BINARY, 
        15, 
        -2
    )

    img_map = cv.resize(img_map, None, fx=4, fy=4, interpolation=cv.INTER_CUBIC)

    #Define the region of interest (ROI)
    x, y, w, h = 240, 280, 120, 700
    roi_gray = img_gray[y:y+h, x:x+w]
    roi_rgb = img_rgb[y:y+h, x:x+w]
    #cv.imshow(f'ROI {i}', roi_rgb)
    #cv.waitKey(0)

    #List of agent names
    agents = ["Astra", "Breach", "Brimstone", "Chamber",
            "Clove", "Cypher", "Deadlock", "Fade", "Gekko", "Harbor", "Iso", 
            "Jett", "Killjoy", "KAYO", "Neon", "Omen", "Phoenix", "Raze", 
            "Reyna", "Sage", "Skye", "Sova", "Tejo", "Viper", "Vyse", "Yoru"]

    #Store detections
    detections = []

    #Preprocess ROI
    roi_gray = cv.GaussianBlur(roi_gray, (5, 5), 0)
    roi_gray = cv.Canny(roi_gray, 50, 150)

    #Perform template matching for each agent
    for agent in agents:
        template = cv.imread(f'Valorant/ValAgents/{agent}.png', cv.IMREAD_GRAYSCALE)
        if template is None:
            print(f"Template for {agent} not found.")
            continue
        #Apply same filters to templates
        template = cv.GaussianBlur(template, (5, 5), 0)
        template = cv.Canny(template, 50, 150)
        #Attempt multiple scales for matching
        for scale in np.linspace(0.5, 1.5, 10):
            resized_template = cv.resize(template, (0, 0), fx=scale, fy=scale)
            if roi_gray.shape[0] < resized_template.shape[0] or roi_gray.shape[1] < resized_template.shape[1]:
                continue
            res = cv.matchTemplate(roi_gray, resized_template, cv.TM_CCOEFF_NORMED)
            threshold = 0.15
            loc = np.where(res >= threshold)
            for pt in zip(*loc[::-1]):
                score = res[pt[1], pt[0]]
                detected_w, detected_h = resized_template.shape[::-1]
                if detected_w < 60 and detected_w > 45 and detected_h <  60 and detected_h > 45:
                    detections.append((score, agent, (pt[0] + x, pt[1] + y), resized_template.shape[::-1]))

    #Sort detections by score
    detections = sorted(detections, key=lambda x: x[0], reverse=True)

    #Apply non-maximum suppression to filter out overlapping detections
    def non_max_suppression(detections, overlap_thresh=0.05):
        if len(detections) == 0:
            return []

        boxes = np.array([(*pt, pt[0] + w, pt[1] + h) for _, _, pt, (w, h) in detections])
        scores = np.array([score for score, _, _, _ in detections])

        x1 = boxes[:, 0]
        y1 = boxes[:, 1]
        x2 = boxes[:, 2]
        y2 = boxes[:, 3]

        area = (x2 - x1 + 1) * (y2 - y1 + 1)
        idxs = np.argsort(scores)[::-1]

        pick = []
        while len(idxs) > 0:
            i = idxs[0]
            pick.append(i)
            xx1 = np.maximum(x1[i], x1[idxs[1:]])
            yy1 = np.maximum(y1[i], y1[idxs[1:]])
            xx2 = np.minimum(x2[i], x2[idxs[1:]])
            yy2 = np.minimum(y2[i], y2[idxs[1:]])

            w = np.maximum(0, xx2 - xx1 + 1)
            h = np.maximum(0, yy2 - yy1 + 1)

            overlap = (w * h) / area[idxs[1:]]

            idxs = idxs[np.where(overlap <= overlap_thresh)[0] + 1]

        return [detections[i] for i in pick]

    filtered_detections = non_max_suppression(detections)

    #Limit of 2 duplicates per agent
    agent_counts = {}
    final_detections = []
    for detection in filtered_detections:
        _, agent, _, _ = detection
        if agent not in agent_counts:
            agent_counts[agent] = 0
        if agent_counts[agent] < 2:
            final_detections.append(detection)
            agent_counts[agent] += 1


    #print(f"Pre filter: {final_detections}")
    detections_copy = final_detections.copy()
    sum = 0
    cnt = 0
    for _, _, top_left, _ in detections_copy:
        sum += top_left[0]
        cnt += 1
    avg = sum / cnt
    for score, agent, top_left, (w, h) in detections_copy:
        if top_left[0] > np.int64(avg + 5) or top_left[0] < np.int64(avg - 5):
            final_detections.remove((score, agent, top_left, (w, h)))
        
    final_detections = non_max_suppression(final_detections)
    
    #Ensure no less than 10 detections
    if len(final_detections) < 10:
        remaining_detections = [d for d in detections if d not in final_detections]
        remaining_detections = sorted(remaining_detections, key=lambda x: x[0], reverse=True)
        for detection in remaining_detections:
            _, agent, _, _ = detection
            if agent_counts.get(agent, 0) < 2:
                final_detections.append(detection)
                agent_counts[agent] = agent_counts.get(agent, 0) + 1
            if len(final_detections) == 10:
                break

    #Draw the top 10 matches' rectangles
    final_detections = final_detections[:10]
    #print(f"Post filter: {final_detections}")
    if len(final_detections) != 10:
        print(f"Error: {len(final_detections)} detections found.")
        continue
    img_result = img_rgb.copy()
    final_detections = sorted(final_detections, key=lambda x: x[2][1])
    for score, agent, top_left, (w, h) in final_detections:
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv.rectangle(img_result, top_left, bottom_right, (0, 255, 0), 2)
        cv.putText(img_result, f'{agent} ({score:.2f})', (top_left[0], top_left[1] - 10),
                cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        

        #Define ROI for OCR
        strip_x = top_left[0] + w
        strip_y = top_left[1] + 10
        strip_w = 1200
        strip_h = h - 20
        strip = img_rgb[strip_y:strip_y + strip_h, strip_x:strip_x + strip_w]
        #cv.imshow(f'OCR ROI {agent}', strip)
        #cv.waitKey(0)


        strip_gray = cv.cvtColor(strip, cv.COLOR_BGR2GRAY)
        strip_gray = cv.adaptiveThreshold(
        strip_gray, 
        255,
        cv.ADAPTIVE_THRESH_MEAN_C, 
        cv.THRESH_BINARY, 
        15, 
        -2
    )
        #strip_gray = cv.GaussianBlur(strip_gray, (5, 5), 0)
        #strip_gray = cv.Canny(strip_gray, 50, 150)
        #cv.imshow(f'OCR ROI PostProc {agent}', strip_gray)
        #cv.waitKey(0)

        strip_name = strip_gray[:, :200]
        strip_stats = strip_gray[:, 300:]
        strip_acs = strip_stats[:, :180]
        strip_kda = strip_stats[:, 180:360]
        strip_econ = strip_stats[:, 360:540]
        strip_fb = strip_stats[:, 540:620]
        strip_p = strip_stats[:, 620:800]
        strip_d = strip_stats[:, 800:]

        #cv.imshow(f'OCR MAP NAME', img_map)
        #cv.waitKey(0)

        #cv.imshow(f'OCR ROI NAME {agent}', strip_name)
        #cv.waitKey(0)

        #cv.imshow(f'OCR ROI ACS {agent}', strip_acs)
        #cv.waitKey(0)

        #cv.imshow(f'OCR ROI KDA {agent}', strip_kda)
        #cv.waitKey(0)

        #cv.imshow(f'OCR ROI Econ {agent}', strip_econ)
        #cv.waitKey(0)

        #cv.imshow(f'OCR ROI FB {agent}', strip_fb)
        #cv.waitKey(0)
        
        #cv.imshow(f'OCR ROI P {agent}', strip_p)
        #cv.waitKey(0)

        #cv.imshow(f'OCR ROI D {agent}', strip_d)
        #cv.waitKey(0)


        ocr_map = pytesseract.image_to_string(img_map, config='--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        ocr_name = pytesseract.image_to_string(strip_gray, config='--psm 7 -c tessedit_char_whitelist="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234456789"')
        ocr_acs = pytesseract.image_to_string(strip_acs, config='--psm 7 -c tessedit_char_whitelist=0123456789')
        ocr_kda = pytesseract.image_to_string(strip_kda, config='--psm 7 -c tessedit_char_whitelist=0123456789/')
        ocr_econ = pytesseract.image_to_string(strip_econ, config='--psm 7 -c tessedit_char_whitelist=0123456789')
        ocr_fb = pytesseract.image_to_string(strip_fb, config='--psm 7 -c tessedit_char_whitelist=0123456789')
        ocr_p = pytesseract.image_to_string(strip_p, config='--psm 7 -c tessedit_char_whitelist=0123456789')
        ocr_d = pytesseract.image_to_string(strip_d, config='--psm 7 -c tessedit_char_whitelist=0123456789')
        print(f"Map: {ocr_map.strip()}")
        print(f"OCR Stats for {ocr_name.split(' ')[0]} on {agent}: {ocr_acs.strip()}, {ocr_kda.strip()}, {ocr_econ.strip()}, {ocr_fb.strip()}, {ocr_p.strip()}, {ocr_d.strip()}")
        players[ocr_name.strip()] = ocr_acs.strip(), ocr_kda, ocr_econ.split('/'), ocr_fb.strip(), ocr_p.strip(), ocr_d.strip()

        cv.rectangle(img_result, (strip_x, strip_y), (strip_x + strip_w, strip_y + strip_h), (255, 0, 0), 2)
        cv.putText(img_result, f'{ocr_name.strip()}', (strip_x, strip_y + 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        cv.putText(img_result, f'ACS: {ocr_acs.strip()}', (strip_x + 360, strip_y+ 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        cv.putText(img_result, f'KDA: {ocr_kda}', (strip_x + 480, strip_y+ 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        cv.putText(img_result, f'Econ: {ocr_econ.strip()}', (strip_x + 600, strip_y+ 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        cv.putText(img_result, f'FB: {ocr_fb.strip()}', (strip_x + 700, strip_y+ 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        cv.putText(img_result, f'Plants: {ocr_p.strip()}', (strip_x + 800, strip_y+ 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        cv.putText(img_result, f'Defuses: {ocr_d.strip()}', (strip_x + 900, strip_y+ 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)


    #Save result
    output_path = f'Valorant/ValMatch/scoreboard_result{i}.png'
    #cv.imshow('Result', img_result)
    #cv.waitKey(0)
    cv.imwrite(output_path, img_result)
    print(players)

    #Print results
    print(f"Top 10 detections for scoreboard {i}:")
    for i, (score, agent, top_left, _) in enumerate(final_detections, 1):
        print(f"{i}. Agent: {agent}, Score: {score:.2f}, Location: {top_left[0], top_left[1]}")

    print(f"Result saved to: {output_path}")