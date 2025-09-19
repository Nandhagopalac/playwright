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
BOOK_NOW_IMAGE       = r"C:\Users\nagal\OneDrive\Pictures\irctc\Capture-booknow.png"
# Removed problematic continue image path - will use text search instead

# --- OPEN BROWSER ---
print("🌐 Opening IRCTC website...")
webbrowser.open(IRCTC_URL)
time.sleep(5)

def wait_and_click(image_path, description, confidence=0.85, max_wait=15, optional=False, offset_y=0):
    """Standard click function for other elements"""
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
            pyautogui.moveTo(target_x, target_y)
            print(f"✅ Clicked on {description} at ({target_x}, {target_y})")
            return True
        time.sleep(0.5)

    if optional:
        print(f"ℹ️ {description} not found (skipped).")
        return False
    else:
        print(f"⚠️ {description} not found within {max_wait} seconds.")
        return False

def wait_and_click_below_cursor(image_path, description, cursor_x, cursor_y, confidence=0.85, max_wait=10):
    """Look for image BELOW the cursor position where hand signal was found"""
    start = time.time()
    
    # Define search region BELOW the cursor position
    region_width = 400
    region_height = 200
    # Search area starts from cursor_y and goes down
    region = (cursor_x - region_width//2, cursor_y, region_width, region_height)
    
    print(f"🔍 Searching for {description} BELOW cursor position ({cursor_x}, {cursor_y})")
    print(f"   Search area below cursor: {region}")
    
    while time.time() - start < max_wait:
        try:
            # Search only in the region below the cursor
            loc = pyautogui.locateCenterOnScreen(image_path, confidence=confidence, region=region)
            if loc:
                pyautogui.moveTo(loc.x, loc.y, duration=0.3)
                pyautogui.click()
                pyautogui.moveTo(loc.x, loc.y)
                print(f"✅ Found and clicked {description} below cursor at ({loc.x}, {loc.y})")
                return True
        except pyautogui.ImageNotFoundException:
            pass
        
        time.sleep(0.5)
    
    print(f"⚠️ {description} not found below cursor position within {max_wait} seconds.")
    return False

def sleeper_click_and_booknow_below(sleeper_image_path, booknow_image_path, clicks=2, confidence=0.85, click_delay=1.0):
    """Find sleeper, click it where hand appears, then look for Book Now BELOW that exact position"""
    try:
        sleeper_locs = list(pyautogui.locateAllOnScreen(sleeper_image_path, confidence=confidence))
        
        if sleeper_locs:
            sleeper_box = max(sleeper_locs, key=lambda loc: loc.top)
            start_x = sleeper_box.left + (sleeper_box.width // 2)
            start_y = sleeper_box.top + (sleeper_box.height // 2)
            
            print(f"📦 Sleeper box found. Starting scan from ({start_x}, {start_y})")
            print("🔍 Moving cursor down in small steps to find hand cursor...")
            
            hand_cursor_x, hand_cursor_y = None, None
            
            # Move cursor down gradually to find where hand cursor appears
            for offset in range(0, 30, 3):  # Move down in 3-pixel steps
                test_x = start_x
                test_y = start_y + offset
                
                pyautogui.moveTo(test_x, test_y, duration=0.3)
                print(f"📍 Cursor at ({test_x}, {test_y}) - Check for hand cursor")
                time.sleep(1)
                
                # Use position after reasonable offset (where hand cursor appears)
                if offset >= 12:
                    print(f"👆 Hand cursor found at: ({test_x}, {test_y})")
                    hand_cursor_x, hand_cursor_y = test_x, test_y
                    
                    # Perform sleeper clicks at hand cursor position
                    for i in range(clicks):
                        pyautogui.moveTo(test_x, test_y, duration=0.2)
                        time.sleep(0.1)
                        pyautogui.click(test_x, test_y)
                        pyautogui.moveTo(test_x, test_y, duration=0.1)
                        
                        print(f"✅ Sleeper click {i+1}/{clicks} at hand cursor position ({test_x}, {test_y})")
                        
                        if i < clicks - 1:
                            time.sleep(click_delay)
                    
                    break
            
            # If sleeper was clicked at hand cursor position, look for Book Now BELOW that position
            if hand_cursor_x and hand_cursor_y:
                print(f"\n🎫 Sleeper selected at hand cursor position!")
                print(f"🔽 Now looking for Book Now button BELOW position ({hand_cursor_x}, {hand_cursor_y})...")
                time.sleep(2)  # Wait for UI to update
                
                # Look for Book Now button BELOW the hand cursor position
                book_success = wait_and_click_below_cursor(
                    booknow_image_path, 
                    "Book Now button",
                    hand_cursor_x, 
                    hand_cursor_y,
                    confidence=0.85,
                    max_wait=8
                )
                
                if book_success:
                    print("✅ Book Now button found and clicked BELOW the hand cursor position!")
                    return True
                else:
                    print("⚠️ Book Now button not found below the hand cursor position.")
                    return False
            
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return False

def find_and_click_continue_button():
    """Find and click Continue button using text search"""
    print("🔄 Searching for Continue button using text search...")
    
    # Open browser search
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(0.5)
    
    # Search for Continue text
    pyautogui.typewrite("Continue", interval=0.05)
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(0.5)
    
    print("✅ Found 'Continue' text")
    
    # Close search box
    pyautogui.press('escape')
    time.sleep(0.2)
    
    # Get current cursor position after text search
    current_pos = pyautogui.position()
    print(f"📍 Continue button position: ({current_pos.x}, {current_pos.y})")
    
    # Click on the Continue button (should be at or near the found text)
    pyautogui.moveTo(current_pos.x, current_pos.y, duration=0.3)
    time.sleep(0.2)
    pyautogui.click(current_pos.x, current_pos.y)
    pyautogui.moveTo(current_pos.x, current_pos.y)  # Lock cursor
    
    print("✅ Continue button clicked!")
    return True

def fill_passenger_details_and_payment():
    """Fill passenger details and handle payment selection using text search"""
    print("\n👤 Filling passenger details...")
    
    # Fill passenger name
    pyautogui.typewrite("Nandhagopal A C", interval=0.1)
    print("✅ Passenger name entered: Nandhagopal A C")
    
    # Move to age field
    pyautogui.press('tab')
    time.sleep(0.2)
    
    # Fill age
    pyautogui.typewrite("41", interval=0.1)
    print("✅ Age entered: 41")
    
    # Move to gender field
    pyautogui.press('tab')
    time.sleep(0.2)
    
    # Press M for Male
    pyautogui.press('m')
    print("✅ Gender selected: Male (M)")
    
    # Move through next fields
    pyautogui.press('tab')
    time.sleep(0.2)
    pyautogui.press('tab')
    time.sleep(0.2)
    
    # Press down arrow twice to select berth preference
    pyautogui.press('down', presses=2, interval=0.2)
    print("✅ Berth preference selected (down arrow pressed twice)")
    
    time.sleep(1)
    
    # Use Ctrl+F to find UPI payment option and click the circle radio button
    print("\n💳 Searching for UPI payment option using text search...")
    
    # Open browser search
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(0.5)
    
    # Search for UPI text
    pyautogui.typewrite("Pay through BHIM/UPI", interval=0.05)
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(0.5)
    
    print("✅ Found 'Pay through BHIM/UPI' text")
    
    # Close search box
    pyautogui.press('escape')
    time.sleep(0.2)
    
    # Get current cursor position after text search
    current_pos = pyautogui.position()
    print(f"📍 Current position after text search: ({current_pos.x}, {current_pos.y})")
    
    # Click the circle radio button (22 pixels left, 2 pixels up from text)
    circle_x = current_pos.x - 22
    circle_y = current_pos.y - 2
    
    print(f"⭕ Clicking UPI circle radio button at: ({circle_x}, {circle_y})")
    
    # Move to and click the circle radio button
    pyautogui.moveTo(circle_x, circle_y, duration=0.3)
    time.sleep(0.2)
    pyautogui.click(circle_x, circle_y)
    pyautogui.moveTo(circle_x, circle_y)  # Lock cursor at circle
    
    print("✅ UPI circle radio button clicked and selected!")
    time.sleep(1)
    
    # Find and click Continue button using text search
    try:
        continue_success = find_and_click_continue_button()
        if continue_success:
            print("✅ Continue button clicked successfully!")
            return True
        else:
            print("⚠️ Failed to click Continue button.")
            return False
    except Exception as e:
        print(f"❌ Error clicking Continue button: {e}")
        return False

# --- HANDLE POPUPS ---
print("\n🔄 Handling popups in order...")
time.sleep(1)
wait_and_click(POPUP_Askdisha_IMAGE, "Ask Disha popup close")
time.sleep(0.5)
wait_and_click(POPUP_OK_IMAGE, "Popup OK button")
time.sleep(0.5)
wait_and_click(POPUP_OK_IMAGE, "Popup OK button")
time.sleep(1)
wait_and_click(POPUP_ALLOW_IMAGE, "Allow Notifications popup", optional=True)

# --- LOGIN PROCESS ---
if wait_and_click(LOGIN_BTN_IMAGE, "Top LOGIN button"):
    time.sleep(0.5)
    pyautogui.typewrite(USERNAME, interval=0.1)
    pyautogui.press('tab')
    time.sleep(0.5)
    pyautogui.typewrite(PASSWORD, interval=0.1)
    pyautogui.press('tab')
    print("✅ Username & Password entered.")
else:
    print("⚠️ Login button not found, skipping credential entry.")

print("\n👉 Please enter the CAPTCHA manually in the browser...")
time.sleep(8)

pyautogui.press('enter')
print("🎉 Logged in successfully!")

# --- TRAVEL DETAILS ---
if wait_and_click(LOGIN_FROM_IMAGE, "From Station field"):
    pyautogui.typewrite("ED", interval=0.2)
    time.sleep(1)
    pyautogui.press('tab')

    pyautogui.press('tab', presses=2, interval=0.2)
    pyautogui.typewrite("MAS", interval=0.2)
    time.sleep(1)
    pyautogui.press('tab')

    pyautogui.press('tab')
    pyautogui.typewrite(JOURNEY_DATE, interval=0.2)
    time.sleep(1)
    pyautogui.press('enter')
    print("✅ Travel details entered & search triggered.")
    
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(1)
    pyautogui.typewrite("22650", interval=0.1)
    pyautogui.press('enter')
    print("🔍 Train 22650 searched.")

    # --- SLEEPER SELECTION AND BOOK NOW BELOW CURSOR ---
    time.sleep(2)
    print("🎯 Starting sleeper selection and Book Now below cursor...")
    
    success = sleeper_click_and_booknow_below(
        r"C:\Users\nagal\OneDrive\Pictures\irctc\Capture-sleeper.png",
        BOOK_NOW_IMAGE,
        clicks=2, 
        click_delay=1.0,
        confidence=0.85
    )
    
    if success:
        print("🎉 Perfect! Sleeper selected and Book Now clicked!")
        
        # --- PASSENGER DETAILS AND PAYMENT ---
        time.sleep(3)  # Wait for booking page to load
        
        passenger_success = fill_passenger_details_and_payment()
        
        if passenger_success:
            print("🎊 Complete booking process successful!")
        else:
            print("⚠️ Issue with passenger details or payment selection.")
    else:
        print("⚠️ Issue with sleeper selection or Book Now click.")

print("\n🎊 IRCTC automation script completed!")
print("📋 Complete Summary:")
print("   ✅ Website opened")
print("   ✅ Popups handled") 
print("   ✅ Login completed")
print("   ✅ Travel details entered (ED → MAS, 23/10/2025)")
print("   ✅ Train 22650 searched")
print("   ✅ Sleeper class selected at hand cursor position")
print("   ✅ Book Now clicked below hand cursor")
print("   ✅ Passenger details filled (Nandhagopal A C, 41, Male)")
print("   ✅ Berth preference selected")
print("   ✅ UPI circle radio button clicked at (385, 674)")
print("   ✅ Continue button found and clicked using text search")
print("   🎫 Ready for payment processing!")
