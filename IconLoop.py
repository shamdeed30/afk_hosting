import cv2 as cv
import numpy as np


#Load screenshot
for i in range(8):
    img_rgb = cv.imread(f'Valorant/Scoreboards/{i}.png')
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)

    #Define the region of interest (ROI)
    x, y, w, h = 240, 280, 120, 660
    roi_gray = img_gray[y:y+h, x:x+w]
    roi_rgb = img_rgb[y:y+h, x:x+w]
    #cv.imshow('ROI', roi_rgb)
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
                detections.append((score, agent, (pt[0] + x, pt[1] + y), resized_template.shape[::-1]))

    #Sort detections by score
    detections = sorted(detections, key=lambda x: x[0], reverse=True)

    #Apply non-maximum suppression to filter out overlapping detections
    def non_max_suppression(detections, overlap_thresh=0.3):
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


    #Remove any detections outside of acceptable X range
    img_result = img_rgb.copy()
    print(f"Pre filter: {final_detections}")
    detections_copy = final_detections.copy()
    sum = 0
    cnt = 0
    for _, _, top_left, _ in detections_copy:
        sum += top_left[0]
        cnt += 1
    for score, agent, top_left, (w, h) in detections_copy:
        if top_left[0] > np.int64(285) or top_left[0] < np.int64(265):
            final_detections.remove((score, agent, top_left, (w, h)))
        
    #final_detections = non_max_suppression(final_detections)
    
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
    print(f"Post filter: {final_detections}")
    for score, agent, top_left, (w, h) in final_detections:
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv.rectangle(img_result, top_left, bottom_right, (0, 255, 0), 2)
        cv.putText(img_result, f'{agent} ({score:.2f})', (top_left[0], top_left[1] - 10),
                cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    #Save result
    output_path = f'Valorant/ValMatch/scoreboard_result{i}.png'
    #cv.imshow('Result', img_result)
    #cv.waitKey(0)
    cv.imwrite(output_path, img_result)

    #Print results
    print(f"Top detections for scoreboard {i}:")
    for i, (score, agent, top_left, _) in enumerate(final_detections, 1):
        print(f"{i}. Agent: {agent}, Score: {score:.2f}, Location: {top_left[0]}")

    print(f"Result saved to: {output_path}")