import pyautogui
import time
import webbrowser
import os

pyautogui.FAILSAFE = True  # Move mouse to corner to stop
pyautogui.PAUSE = 1        # Add a 1-sec pause after each action

# --- CONFIG ---
gmail_url = "https://mail.google.com"
recipient_email = "muzaffar.ahamed86@gmail.com"
subject_text = "Automated Email from PyAutoGUI"
message_body = "Hello,\n\nThis is an automated email sent using Python and PyAutoGUI.\n\nBest regards,\nMuzaffar"

# --- STEP 1: Open Gmail ---
print("Opening Gmail...")
webbrowser.open(gmail_url)
time.sleep(10)  # Wait for Gmail to load

# --- STEP 2: Click Compose ---
print("Locating Compose button...")
compose_button = pyautogui.locateCenterOnScreen('compose_button.png', confidence=0.8)
if compose_button:
    pyautogui.click(compose_button)
    time.sleep(3)
else:
    print("Compose button not found!")
    exit()

# --- STEP 3: Enter Recipient ---
print("Typing recipient...")
pyautogui.typewrite(recipient_email)
pyautogui.press('enter')
pyautogui.press('tab')  # Move to subject field
time.sleep(1)

# --- STEP 4: Enter Subject ---
pyautogui.typewrite(subject_text)
pyautogui.press('tab')  # Move to message body
time.sleep(1)

# --- STEP 5: Enter Message ---
pyautogui.typewrite(message_body)

# --- STEP 6: Send Email ---
print("Sending email...")
send_button = pyautogui.locateCenterOnScreen('send_button.png', confidence=0.8)
if send_button:
    pyautogui.click(send_button)
    print("✅ Email sent successfully!")
else:
    print("Send button not found.")
