import csv
import time
import datetime
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
# replace username with your
# chrome_options.add_argument("--user-data-dir=/home/username/.config/google-chrome")  # Linux
chrome_options.add_argument("--user-data-dir=C:\\Users\\Prashanna\\AppData\\Local\\Google\\Chrome\\User Data")  # Windows

# Add the profile directory (if using a specific profile)
chrome_options.add_argument("--profile-directory=Default")
# Replace "Default" with your profile name if needed or if you have multiple profiles write(Profile 1, Profile 2)
# look for profiles in path:C:\Users\Prashanna\AppData\Local\Google\Chrome\User Data
# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.maximize_window()
time.sleep(5)  # Shortened wait time for browser to load

# # Switch to the new tab
def is_whatsapp_open(driver):
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if "web.whatsapp.com" in driver.current_url:
            print("WhatsApp Web is already open in a tab.")
            return True
    return False

# Check if WhatsApp Web is already open
if not is_whatsapp_open(driver):
    print("WhatsApp Web is not open. Opening a new tab...")
    driver.execute_script("window.open('');")  # Open a new blank tab
    driver.switch_to.window(driver.window_handles[-1])  # Switch to the new tab
    driver.get("https://web.whatsapp.com")  # Open WhatsApp Web in the new tab
    print("Waiting for WhatsApp Web to load...")
    time.sleep(10)  # Adjust the delay as needed
else:
    print("Switching to the existing WhatsApp Web tab.")

print("Scan the QR Code and press Enter after logging in.")
input("Press Enter after scanning QR Code and logging in: ")

# Generate filename for logs
log_file = "sent_messages_log.csv"
current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
failed_contacts_file = f"failed_contacts_{current_time}.csv"

# Ensure log files exist
if not os.path.exists(log_file):
    with open(log_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Phone Number", "Message", "Timestamp"])

if not os.path.exists(failed_contacts_file):
    with open(failed_contacts_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Phone Number", "Timestamp"])


# Function to check if a message has already been sent
def is_already_sent(phone_number, message):
    with open(log_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if row and row[0] == phone_number and row[1] == message:
                return True
    return False


# Function to log sent messages
def log_sent_message(phone_number, message):
    with open(log_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([phone_number, message, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])


# Function to log failed contacts
def log_failed_contact(phone_number):
    with open(failed_contacts_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([phone_number, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])


# Function to send messages
def sendMsg(phone_number, message):
    if is_already_sent(phone_number, message):
        print(f"Message already sent to {phone_number}, skipping...")
        return

    print(f"Sending message to {phone_number}...")
    try:
        driver.get(f"https://web.whatsapp.com/send?phone={phone_number}&text={message}")

        input_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
        )
        input_box.clear()
        input_box.send_keys(message)

        send_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Send"]'))
        )
        send_button.click()
        print(f"Message sent to {phone_number} successfully!")
        log_sent_message(phone_number, message)
        time.sleep(5)
    except Exception as e:
        print(f"Failed to send message to {phone_number}: {e}")
        log_failed_contact(phone_number)

# Function to send images or videos
def send_media(phone_number, file_path,caption, is_video=False):
    if is_already_sent(phone_number, file_path):
        print(f"Attachment already sent to {phone_number}, skipping...")
        return
    print(f"Sending {'video' if is_video else 'image'} to {phone_number}...")
    try:

        driver.get(f"https://web.whatsapp.com/send?phone={phone_number}")

        # Wait for the attachment button to load
        attachment_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="plus"]'))
        )
        attachment_button.click()
        # Wait for the file input element to load
        file_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'))
        )
        file_input.send_keys(file_path)
        time.sleep(10) #delay for large files
        # Wait for the caption input box to load
        caption_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@aria-label="Add a caption"]'))
        )
        caption_box.send_keys(caption)
        print("Caption added.")
        time.sleep(2)  # Wait for the caption to be typed
        # Wait for the Send button to be clickable
        send_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]'))
        )
        send_button.click()
        print(f"{'Video' if is_video else 'Image'} sent to {phone_number} successfully!")
        log_sent_message(phone_number, file_path)
        time.sleep(5)
    except Exception as e:
        print(f"Failed to send {'video' if is_video else 'image'} to {phone_number}: {e}")


# Option 1: Send messages from a hardcoded list
contacts = [
    "+9779842724655",
]
message = "Hello! This is an automated message sent using Selenium."
# Path to image or video file
image_path = "C:/Users/Prashanna/OneDrive/Pictures/C Module/classwork.jpg"
video_path = "C:/Users/Prashanna/Videos/trip.mp4"
image_caption_message="this is image caption message"
video_caption_message="this is video caption message"

# Option 2: Read contacts from CSV file
def read_contacts_from_csv(filename):
    contacts_from_csv = []
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if row:
                    contacts_from_csv.append(row[0])  # Assuming phone numbers are in the first column
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    return contacts_from_csv


# Choose option: Hardcoded list or CSV file
use_csv = input("Do you want to use a CSV file for contacts? (yes/no): ").strip().lower()
if use_csv == "yes":
    csv_file = "./contacts.csv"  # Modify this if needed
    contacts = read_contacts_from_csv(csv_file)

print(f"Total contacts: {len(contacts)}")
for phone_number in contacts:
    sendMsg(phone_number, message)
    # Send image
    if os.path.exists(image_path):
        send_media(phone_number, image_path,image_caption_message, is_video=False)
    else:
        print(f"Image file not found: {image_path}")

    # Send video
    if os.path.exists(video_path):
        send_media(phone_number, video_path,video_caption_message, is_video=True)
    else:
        print(f"Video file not found: {video_path}")
    time.sleep(3)

print("All messages sent. Closing browser...")
driver.quit()
