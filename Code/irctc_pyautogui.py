import pyautogui
import webbrowser
import time

# --- SETTINGS ---
IRCTC_URL = "https://www.irctc.co.in/nget/train-search"
USERNAME = "ayyampudur"
PASSWORD = "Agalya@253520"
JOURNEY_DATE = "23/10/2025"

# Screenshot images
POPUP_Askdisha_IMAGE = r"C:\Users\nagal\OneDrive\Pictures\irctc\Capture-Close.png"
POPUP_OK_IMAGE       = r"C:\Users\nagal\OneDrive\Pictures\irctc\Capture-OK.png"
POPUP_ALLOW_IMAGE    = r"C:\Users\nagal\OneDrive\Pictures\irctc\Capture-Allow.png"
LOGIN_BTN_IMAGE      = r"C:\Users\nagal\OneDrive\Pictures\irctc\Capture-login.png"
LOGIN_FROM_IMAGE     = r"C:\Users\nagal\OneDrive\Pictures\irctc\Capture-from.png"

# --- OPEN BROWSER ---
print("🌐 Opening IRCTC website...")
webbrowser.open(IRCTC_URL)
time.sleep(5)  # allow page to fully load

def wait_and_click(image_path, description, confidence=0.85, max_wait=15, optional=False, offset_y=0):
    """Wait until an image appears on the screen, then click it.
       If optional=True, skip silently when not found."""
    start = time.time()
    while time.time() - start < max_wait:
        try:
            loc = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
        except pyautogui.ImageNotFoundException:
            loc = None

        if loc:
            target_x, target_y = loc.x, loc.y + offset_y
            pyautogui.moveTo(target_x, target_y, duration=0.2)
            pyautogui.click()
            pyautogui.moveTo(target_x, target_y)  # 👈 reset cursor to same spot
            print(f"✅ Clicked on {description} at ({target_x}, {target_y})")
            return True
        time.sleep(0.5)

    if optional:
        print(f"ℹ️ {description} not found (skipped).")
        return False
    else:
        print(f"⚠️ {description} not found within {max_wait} seconds.")
        return False

# --- HANDLE POPUPS (strict order) ---
print("\n🔄 Handling popups in order...")
time.sleep(1)
wait_and_click(POPUP_Askdisha_IMAGE, "Ask Disha popup close")
time.sleep(0.5)
wait_and_click(POPUP_OK_IMAGE, "Popup OK button")
time.sleep(0.5)
wait_and_click(POPUP_OK_IMAGE, "Popup OK button")
time.sleep(1)
wait_and_click(POPUP_ALLOW_IMAGE, "Allow Notifications popup", optional=True)

# --- CLICK LOGIN BUTTON ---
if wait_and_click(LOGIN_BTN_IMAGE, "Top LOGIN button"):
    time.sleep(0.5)  # wait for login box to load

    # --- ENTER USERNAME + PASSWORD ---
    pyautogui.typewrite(USERNAME, interval=0.1)
    pyautogui.press('tab')
    time.sleep(0.5)
    pyautogui.typewrite(PASSWORD, interval=0.1)
    pyautogui.press('tab')
    print("✅ Username & Password entered.")
else:
    print("⚠️ Login button not found, skipping credential entry.")

# --- WAIT FOR CAPTCHA (manual step) ---
print("\n👉 Please enter the CAPTCHA manually in the browser...")
time.sleep(8)  # give enough time for user to type captcha

# --- CLICK SIGN IN ---
pyautogui.press('enter')
print("🎉 Logged in successfully!")

# --- ENTER TRAVEL DETAILS ---
if wait_and_click(LOGIN_FROM_IMAGE, "From Station field"):
    # From station
    pyautogui.typewrite("ED", interval=0.2)
    time.sleep(1)
    pyautogui.press('tab')

    # To station
    pyautogui.press('tab', presses=2, interval=0.2)
    pyautogui.typewrite("MAS", interval=0.2)
    time.sleep(1)
    pyautogui.press('tab')

    # Date
    pyautogui.press('tab')
    pyautogui.typewrite(JOURNEY_DATE, interval=0.2)
    time.sleep(1)
    # Submit
    pyautogui.press('enter')
    print("✅ Travel details entered & search triggered.")
    # --- EXTRA STEPS: Search Train & Click Sleeper ---
    time.sleep(1)  # wait for results to load
    pyautogui.hotkey('ctrl', 'f')  # open browser search
    time.sleep(1)
    pyautogui.typewrite("22650", interval=0.1)
    pyautogui.press('enter')
    print("🔍 Train 22650 searched.")

        # Locate and click Sleeper (SL) AFTER first occurrence of train
    # Locate and click Sleeper (SL) AFTER first occurrence of train
# Locate and click Sleeper (SL) AFTER first occurrence of train
# Locate and click Sleeper (SL) AFTER first occurrence of train
time.sleep(2)
try:
    sleeper_locs = list(pyautogui.locateAllOnScreen(
        r"C:\Users\nagal\OneDrive\Pictures\irctc\Capture-sleeper.png", 
        confidence=0.85
    ))
    if sleeper_locs:
        # pick the lowest one (largest y) → usually the one after 22650
        sleeper_loc = max(sleeper_locs, key=lambda loc: loc.top)
        center = pyautogui.center(sleeper_loc)

        # --- First click ---
        pyautogui.mouseDown(center.x, center.y)   # press but don’t release
        time.sleep(0.05)
        pyautogui.mouseUp(center.x, center.y)     # release at same spot
        pyautogui.moveTo(center.x, center.y)      # lock cursor back

        time.sleep(1)

        # --- Second click ---
        pyautogui.mouseDown(center.x, center.y)
        time.sleep(0.05)
        pyautogui.mouseUp(center.x, center.y)
        pyautogui.moveTo(center.x, center.y)      # lock cursor back

        print("✅ Sleeper (SL) clicked twice and cursor stayed fixed.")
    else:
        print("⚠️ Could not find Sleeper (SL) on screen.")
except Exception as e:
    print("⚠️ Error locating Sleeper:", e)
