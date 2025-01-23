import cv2 as cv
import numpy as np

#Load screenshot
img_rgb = cv.imread('Valorant/Val_Scoreboard.png')
img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)

#Define the region of interest (ROI)
x, y, w, h = 265, 332, 60, 530  # Adjust these values as needed
roi_gray = img_gray[y:y+h, x:x+w]
roi_rgb = img_rgb[y:y+h, x:x+w]

#List of agent names
agents = ["Astra", "Breach", "Brimstone", "Chamber",
          "Clove", "Cypher", "Deadlock", "Fade", "Gekko", "Harbor", "Iso", 
          "Jett", "KAYO", "Killjoy", "Neon", "Omen", "Phoenix", "Raze", 
          "Reyna", "Sage", "Skye", "Sova", "Tejo", "Viper", "Vyse", "Yoru"]

detections = []

#Perform template matching for each agent
for agent in agents:
    template = cv.imread(f'Valorant/ValAgents/{agent}.png', cv.IMREAD_GRAYSCALE)
    #Perform template matching using CCOEFF_NORMED
    res = cv.matchTemplate(roi_gray, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.3
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        score = res[pt[1], pt[0]]
        detections.append((score, agent, (pt[0] + x, pt[1] + y), template.shape[::-1]))

#Sort detections by confidence
detections = sorted(detections, key=lambda x: x[0], reverse=True)

#Apply non-maximum suppression to avoid overlapping
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

#Limit to a maximum of 2 duplicates per agent
agent_counts = {}
final_detections = []
for detection in filtered_detections:
    _, agent, _, _ = detection
    if agent not in agent_counts:
        agent_counts[agent] = 0
    if agent_counts[agent] < 2:
        final_detections.append(detection)
        agent_counts[agent] += 1

#Put a rectangle around best matches
img_result = img_rgb.copy()
for score, agent, top_left, (w, h) in final_detections:
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv.rectangle(img_result, top_left, bottom_right, (0, 255, 0), 2)
    cv.putText(img_result, f'{agent} ({score:.2f})', (top_left[0], top_left[1] - 10),
               cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

#Save result
output_path = 'Valorant/ValMatch/scoreboard_result.png'
cv.imwrite(output_path, img_result)

#Print the results, including the location of each agent
print("Top detections:")
for i, (score, agent, top_left, _) in enumerate(final_detections, 1):
    print(f"{i}. Agent: {agent}, Score: {score:.2f}, Location: {top_left}")

print(f"Result saved to: {output_path}")