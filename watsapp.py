import pyautogui
import time

class WhatsAppBot:
    def send_message(self, contact_name, message):
        # Step 1: Open Windows Search (Win + S)
        pyautogui.hotkey('win', 's')
        time.sleep(1)

        # Step 2: Type 'WhatsApp'
        pyautogui.write('WhatsApp', interval=0.1)
        time.sleep(2)

        # Step 3: Locate and click on WhatsApp icon
        whatsapp_icon = pyautogui.locateCenterOnScreen('images\whatsappimage.png', confidence=0.8)
        if whatsapp_icon:
            pyautogui.click(whatsapp_icon)
            print("Clicked on WhatsApp icon.")
        else:
            print("WhatsApp icon not found on screen.")
            exit()

        # Step 4: Wait for WhatsApp to load
        time.sleep(5)
        print("WhatsApp should be loaded now.")

        # Step 5: Type contact name to search
        pyautogui.write(contact_name, interval=0.1)
        print(f"Typed '{contact_name}' in WhatsApp.")

        # Step 6: Tab to highlight the contact, then Enter to open chat
        time.sleep(1)
        pyautogui.press('tab')
        time.sleep(1)
        pyautogui.press('enter')
        print(f"Opened chat with {contact_name}.")

        #  contact_image = pyautogui.locateCenterOnScreen('images\muzaffar_contact.png', confidence=0.8)
         # if contact_image:
        #   pyautogui.click(contact_image)
        #   print("Clicked on Muzaffar contact.")
       #   else:
        #   print("Contact image not found.")


        # Step 7: Type message and press Enter to send
        time.sleep(1)
        pyautogui.write(message, interval=0.1)
        pyautogui.press('enter')
        print(f"Sent '{message}' message.")

# Example usage
if __name__ == "__main__":
    bot = WhatsAppBot()
    bot.send_message(contact_name="SE - AI-B3 - 1", message="At Last! Completed week one assignment using PyAutoGUI.")
