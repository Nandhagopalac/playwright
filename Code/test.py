import pyautogui
import webbrowser
import time
import cv2
import numpy as np

# --- SETTINGS ---
IRCTC_URL = "https://www.irctc.co.in/nget/train-search"
region_top_left = (0, 0, 300, 300)  # (x, y, width, height)

# Open IRCTC website
print("🌐 Opening IRCTC website...")
webbrowser.open(IRCTC_URL)
time.sleep(5)  # wait for site to load

# Take full screenshot
screenshot = pyautogui.screenshot()
img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

# Draw rectangle on the chosen region
x, y, w, h = region_top_left
cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)  # red border

# Show the screenshot with rectangle
cv2.imshow("Check Region (Red Box)", img)
print("👉 Red box shows the scanning region. Close the window when done.")
cv2.waitKey(0)
cv2.destroyAllWindows()
