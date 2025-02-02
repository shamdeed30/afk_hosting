import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img_rgb = cv.imread('Valorant/Val_Scoreboard_Icons.png')
assert img_rgb is not None, "file could not be read, check with os.path.exists()"
img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
agents = ["Astra", "Breach", "Brimstone", "Chamber",
          "Clove", "Cypher", "Deadlock", "Fade", "Gekko", "Harbor", "Iso", 
          "Jett", "Killjoy", "Neon", "Omen", "Phoenix", "Raze", 
          "Reyna", "Sage", "Skye", "Sova", "Tejo", "Viper", "Vyse", "Yoru"]
for agent in agents:
    cp = img_rgb.copy()
    template = cv.imread(f'Valorant/ValAgents0/{agent}.png', cv.IMREAD_GRAYSCALE)
    assert template is not None, "file could not be read, check with os.path.exists()"
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img_gray, template, cv.TM_SQDIFF_NORMED)
    threshold = 0.34999999999
    loc = np.where( res <= threshold)
    for pt in zip(*loc[::-1]):
        cv.rectangle(cp, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

    cv.imwrite(f'Valorant/ValMatch/res{agent}.png',cp)
    print(f"{agent} done.")