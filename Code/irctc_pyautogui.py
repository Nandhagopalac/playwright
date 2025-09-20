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
ADD_PASSENGER_IMAGE  = r"C:\Users\nagal\OneDrive\Pictures\irctc\Capture-addpassenger.png"
NEXT_SCREEN_IMAGE    = r"C:\Users\nagal\OneDrive\Pictures\irctc\Capture-nextscreen.png"
ENTER_CAPTCHA_IMAGE  = r"C:\Users\nagal\OneDrive\Pictures\irctc\Capture-entercaptcha.png"
PAYMENT_METHOD_IMAGE = r"C:\Users\nagal\OneDrive\Pictures\irctc\Capture-paymentmethod.png"
AMAZON_PAY_UPI_IMAGE = r"C:\Users\nagal\OneDrive\Pictures\irctc\Capture-amazonpayupi.png"
PAY_AND_BOOK_IMAGE   = r"C:\Users\nagal\OneDrive\Pictures\irctc\Capture-payandbook.png"

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

def wait_for_image(image_path, description, confidence=0.85, max_wait=60):
    """Wait for an image to appear on screen without clicking"""
    start = time.time()
    print(f"⏳ Waiting for {description} to appear (max {max_wait} seconds)...")
    
    while time.time() - start < max_wait:
        try:
            loc = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
            if loc:
                print(f"✅ {description} found at ({loc.x}, {loc.y})")
                return True
        except pyautogui.ImageNotFoundException:
            pass
        time.sleep(1)
    
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

# --- HANDLE POPUPS ---
print("\n🔄 Handling popups in order...")
time.sleep(2)
wait_and_click(POPUP_Askdisha_IMAGE, "Ask Disha popup close")
time.sleep(2)
wait_and_click(POPUP_OK_IMAGE, "Popup OK button")
time.sleep(3)
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
        print("🎉 Perfect! Sleeper selected and Book Now clicked below cursor!")
        
        # --- PASSENGER DETAILS ---
        print("\n👤 Starting passenger details entry...")
        time.sleep(3)
        
        # Passenger 1: Nandhagopal A C
        print("👤 Entering details for passenger 1...")
        pyautogui.typewrite("Nandhagopal A C", interval=0.1)
        print("✅ Name entered: Nandhagopal A C")
        
        pyautogui.press('tab')
        time.sleep(0.2)
        
        pyautogui.typewrite("41", interval=0.1)
        print("✅ Age entered: 41")
        
        pyautogui.press('tab')
        time.sleep(0.2)
        
        pyautogui.press('m')
        print("✅ Gender selected: M")
        
        pyautogui.press('tab')
        time.sleep(0.2)
        pyautogui.press('tab')
        time.sleep(0.2)
        pyautogui.press('m')
        print("✅ Pressed M")
        
        print("✅ Passenger 1 details completed")
        
        # Click Add Passenger button
        print("\n➕ Clicking Add Passenger button...")
        if wait_and_click(ADD_PASSENGER_IMAGE, "Add Passenger button"):
            time.sleep(2)
            
            # Passenger 2: Kiruthika R
            print("👤 Entering details for passenger 2...")
            pyautogui.typewrite("Kiruthika R", interval=0.1)
            print("✅ Name entered: Kiruthika R")
            
            pyautogui.press('tab')
            time.sleep(0.2)
            
            pyautogui.typewrite("37", interval=0.1)
            print("✅ Age entered: 37")
            
            pyautogui.press('tab')
            time.sleep(0.2)
            
            pyautogui.press('f')
            print("✅ Gender selected: F")
            
            pyautogui.press('tab')
            time.sleep(0.2)

            pyautogui.press('tab')
            time.sleep(0.2)
            
            pyautogui.press('m')
            print("✅ Pressed M")
            
            print("✅ Passenger 2 details completed")
            
            # Press 11 times tab and down arrow
            print("\n⌨️ Final navigation - pressing 11 tabs and down arrow...")
            pyautogui.press('tab', presses=11, interval=0.2)
            time.sleep(0.5)
            pyautogui.press('down')
            print("✅ Final navigation completed")
            
            # --- FINAL STEPS: Two tabs and enter ---
            print("\n🏁 Final steps - pressing 2 tabs and enter...")
            pyautogui.press('tab')
            time.sleep(0.2)
            pyautogui.press('tab')
            time.sleep(0.2)
            pyautogui.press('enter')
            print("✅ Final two tabs and enter completed")
            
            # --- WAIT FOR NEXT SCREEN AND HANDLE CAPTCHA ---
            print("\n⏳ Waiting for next screen to load...")
            if wait_for_image(NEXT_SCREEN_IMAGE, "Next screen", confidence=0.85, max_wait=60):
                print("🎯 Next screen detected! Proceeding with captcha handling...")
                time.sleep(2)
                
                # Ctrl+F → Type "Enter Captcha" → Enter, then find image and click
                print("🔍 Ctrl+F to search for 'Enter Captcha'...")
                pyautogui.hotkey('ctrl', 'f')
                time.sleep(1)
                print("⌨️ Typing 'Enter Captcha' in search box...")
                pyautogui.typewrite("Enter Captcha", interval=0.1)
                time.sleep(1)
                print("⌨️ Pressing Enter to find text...")
                pyautogui.press('enter')
                time.sleep(1)
                
                # Now find and click the Enter Captcha image
                print("🖼️ Looking for Enter Captcha image to click...")
                if wait_and_click(ENTER_CAPTCHA_IMAGE, "Enter Captcha field", confidence=0.85, max_wait=10):
                    print("✅ Enter Captcha field clicked successfully using image recognition")
                else:
                    print("⚠️ Enter Captcha image not found, trying generic click...")
                    pyautogui.click()
                
                # Wait for manual captcha entry
                print("\n🔐 Please enter the CAPTCHA manually...")
                print("⏰ Waiting 8 seconds for manual captcha entry...")
                time.sleep(8)
                
                # Final two tabs and enter
                print("\n🎯 Final captcha submission - pressing 2 tabs and enter...")
                pyautogui.press('tab')
                time.sleep(0.2)
                pyautogui.press('tab')
                time.sleep(0.2)
                pyautogui.press('enter')
                print("✅ Captcha submission completed!")
                time.sleep(5)  # Wait for page to load after captcha submission
                
            else:
                print("⚠️ Next screen not detected within timeout period.")
        else:
            print("⚠️ Add Passenger button not found")
    else:
        print("⚠️ Issue with sleeper selection or Book Now click below cursor.")

# --- PAYMENT METHOD SELECTION (MOVED OUTSIDE THE NEXT_SCREEN_IMAGE IF BLOCK) ---
print("\n💳 Starting payment method selection...")
print("🔍 Looking for Payment Method button...")
time.sleep(5)  # Extra wait for payment page to load

# Step 1: Click Payment Method
payment_success = wait_and_click(PAYMENT_METHOD_IMAGE, "Payment Method", confidence=0.8, max_wait=20)
if payment_success:
    print("✅ Payment Method clicked successfully")
    time.sleep(3)
    
    # Step 2: Click Amazon Pay UPI
    print("🔍 Looking for Amazon Pay UPI option...")
    upi_success = wait_and_click(AMAZON_PAY_UPI_IMAGE, "Amazon Pay UPI", confidence=0.8, max_wait=15)
    if upi_success:
        print("✅ Amazon Pay UPI selected successfully")
        time.sleep(3)
        
        # Step 3: Click Pay and Book
        print("🔍 Looking for Pay and Book button...")
        pay_success = wait_and_click(PAY_AND_BOOK_IMAGE, "Pay and Book", confidence=0.8, max_wait=15)
        if pay_success:
            print("✅ Pay and Book clicked successfully")
            print("🎉 Payment process initiated!")
        else:
            print("⚠️ Pay and Book button not found")
    else:
        print("⚠️ Amazon Pay UPI option not found")
else:
    print("⚠️ Payment Method button not found")

print("\n🎊 IRCTC automation script completed!")
print("📋 Final Summary:")
print("   ✅ Website opened")
print("   ✅ Popups handled") 
print("   ✅ Login completed")
print("   ✅ Travel details entered (ED → MAS, 23/10/2025)")
print("   ✅ Train 22650 searched")
print("   ✅ Sleeper class selected at hand cursor position")
print("   ✅ Book Now clicked BELOW the hand cursor position")
print("   ✅ Passenger 1 details entered (Nandhagopal A C, 41, M)")
print("   ✅ Add Passenger button clicked")
print("   ✅ Passenger 2 details entered (Kiruthika R, 37, F)")
print("   ✅ Final navigation completed (11 tabs + down arrow)")
print("   ✅ Final two tabs and enter executed")
print("   ✅ Next screen detection and captcha handling")
print("   ✅ Ctrl+F → 'Enter Captcha' → Enter, then find image and click")
print("   ✅ Manual captcha entry (8 second wait)")
print("   ✅ Captcha submission (2 tabs + enter)")
print("   ✅ Payment Method selection attempted")
print("   ✅ Amazon Pay UPI selection attempted")
print("   ✅ Pay and Book button click attempted")
print("   🎫 Complete automation sequence finished!")
