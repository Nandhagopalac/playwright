import pyautogui
import webbrowser
import time

# --- SETTINGS ---
IRCTC_URL = "https://www.irctc.co.in/nget/train-search"
USERNAME = "ayyampudur"
PASSWORD = "Agalya@253520"

# Screenshot images (make sure these are exact cropped screenshots!)
POPUP_Askdisha_IMAGE = r"C:\Users\nagal\OneDrive\Pictures\irctc\Capture-Close.png"
POPUP_OK_IMAGE       = r"C:\Users\nagal\OneDrive\Pictures\irctc\Capture-OK.png"
POPUP_ALLOW_IMAGE    = r"C:\Users\nagal\OneDrive\Pictures\irctc\Capture-Allow.png"
LOGIN_BTN_IMAGE      = r"C:\Users\nagal\OneDrive\Pictures\irctc\Capture-login.png"
# USER_FIELD_IMAGE     = r"C:\Users\nagal\OneDrive\Pictures\irctc\login_user_name.png"  # kept for reference, not used

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
            pyautogui.moveTo(loc.x, loc.y + offset_y, duration=0.2)
            pyautogui.click()
            print(f"✅ Clicked on {description} at {loc}")
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

wait_and_click(POPUP_Askdisha_IMAGE, "Ask Disha popup close")
time.sleep(0.5)

wait_and_click(POPUP_OK_IMAGE, "Popup OK button")
time.sleep(0.5)

wait_and_click(POPUP_ALLOW_IMAGE, "Allow Notifications popup", optional=True)

# --- CLICK LOGIN BUTTON ---
if wait_and_click(LOGIN_BTN_IMAGE, "Top LOGIN button"):
    time.sleep(2)  # wait for login box to load

    # --- ENTER USERNAME + PASSWORD (without needing USER_FIELD_IMAGE) ---
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
time.sleep(15)  # give enough time for user to type captcha

# --- CLICK SIGN IN ---
pyautogui.press('enter')
print("🎉 Automation completed successfully!")
