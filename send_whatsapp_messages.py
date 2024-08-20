from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__)

# אתחול של דפדפן Chrome
driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com/")
print("Scan QR code and press Enter.")
input()  # המתן לסריקת QR

@app.route('/send-messages', methods=['POST'])
def send_messages():
    data = request.json
    recipients = data['formattedContacts']
    message = data['message']
    
    responses = []
    
    for recipient in recipients:
        send_message(recipient, message)

    time.sleep(15)

    for recipient in recipients:
        while True:
            try:
                response = wait_for_response(recipient, timeout=10)
                print(f"Responses2: {response}")  # הדפסת הרשומות לפני ההחזרה

                responses.append({'recipient': recipient, 'response': response})
                break  # יציאה מהלולאה אם אין חריגה
            except Exception as e:
                print(f"An error occurred: {e}")
                time.sleep(2)  # המתן זמן קצר לפני ניסיון חוזר

    print(f"Responses: {responses}")  # הדפסת הרשומות לפני ההחזרה
    return jsonify({'success': True, 'responses': responses})

@app.route('/trigger-wait-for-response', methods=['POST'])
def trigger_wait_for_response():
    data = request.json
    recipients = data['recipients']
    
    responses = []

    for recipient in recipients:
        while True:
            try:
                response = wait_for_response(recipient, timeout=10)
                print(f"Response for {recipient}: {response}")  # הדפסת הרשומות לפני ההחזרה

                responses.append({'recipient': recipient, 'response': response})
                break  # יציאה מהלולאה אם אין חריגה
            except Exception as e:
                print(f"An error occurred: {e}")
                time.sleep(2)  # המתן זמן קצר לפני ניסיון חוזר

    print(f"Responses: {responses}")  # הדפסת הרשומות לפני ההחזרה
    return jsonify({'success': True, 'responses': responses})

def send_message(contact_number, message):
    time.sleep(2)
    new_chat_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/header/header/div/span/div/span/div[1]/div/span'))
    )                                          
    new_chat_button.click()
    time.sleep(2)
    search_box = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/div/div[1]/div[2]/div[2]/div/div[1]/p'))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", search_box)
    search_box.click()
    search_box.send_keys(contact_number)
    time.sleep(2)
    search_box.send_keys(Keys.ENTER)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p'))
    )
    time.sleep(1)
    message_box = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')
    message_box.send_keys(message)
    send_button = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span')
    send_button.click()
    time.sleep(1)

    new_menu_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/header/div[3]/div/div[2]/div/div/span'))
    )
    new_menu_button.click()
    time.sleep(1)

    new_clean_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/span[5]/div/ul/div/div/li[6]/div'))
    )
    new_clean_button.click()
    time.sleep(2)

    accept_clean_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div[3]/div/button[2]/div/div'))
    )
    accept_clean_button.click()
    time.sleep(2)

    initial_messages = read_all_messages()

def clean_text(text):
    return text.strip()

def read_all_messages():
    try:
        messages = driver.find_elements(By.XPATH, '//div[contains(@class, "message-in")]//div[@class="copyable-text"]')
        print(f"[clean_text(message.text) for message in messages]: {[clean_text(message.text) for message in messages]}")
        return [clean_text(message.text) for message in messages]

    except Exception as e:
        print(f"Exception occurred while reading messages: {e}")
        return []

def wait_for_response(contact_number, timeout=5):
    new_chat_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/header/header/div/span/div/span/div[1]/div/span'))
    )
    new_chat_button.click()
    time.sleep(2)
    search_box = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/div/div[1]/div[2]/div[2]/div/div[1]/p'))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", search_box)
    search_box.click()
    search_box.send_keys(contact_number)
    time.sleep(2)

    search_box.send_keys(Keys.ENTER)
  
    start_time = time.time()
    while time.time() - start_time < timeout:
        current_messages = read_all_messages()
        print(f"current_messages1: {current_messages}")

        if current_messages:
            return current_messages[-1]

        time.sleep(2)
    return "No response"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
