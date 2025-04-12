from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fpdf import FPDF
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Automatically download and use correct ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

import os

# Secure credentials
UDEMY_EMAIL = os.getenv("UDEMY_EMAIL") or input("Enter Udemy Email: ")
UDEMY_PASSWORD = os.getenv("UDEMY_PASSWORD") or input("Enter Udemy Password: ")

# Set up WebDriver options
chrome_options = Options()
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(options=chrome_options)

def udemy_login():
    """Logs into Udemy."""
    driver.get("https://www.udemy.com/join/login-popup/")
    time.sleep(5)

    try:
        wait = WebDriverWait(driver, 15)

        email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        email_input.send_keys(UDEMY_EMAIL)

        password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        password_input.send_keys(UDEMY_PASSWORD)

        login_button = wait.until(EC.element_to_be_clickable((By.ID, "submit-id-submit")))
        login_button.click()

        print("✅ Udemy Login Successful!")
        time.sleep(5)  # Allow login
    except Exception as e:
        print("❌ Login Failed:", e)
        driver.quit()
        exit()

def get_transcripts(course_url):
    """Fetches transcripts from Udemy video."""
    driver.get(course_url)
    time.sleep(5)

    wait = WebDriverWait(driver, 10)

    try:
        transcript_button = wait.until(EC.element_to_be_clickable((By.ID, "popper-trigger--549")))
        transcript_button.click()
        print("✅ Transcript button clicked!")
        time.sleep(5)
    except:
        print("⚠️ Transcript button not found. Trying 'Next'.")
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, '[data-purpose="go-to-next"]')
            next_button.click()
        except:
            print("❌ No transcript or next button.")

    transcripts = []
    transcript_elements = driver.find_elements(By.CSS_SELECTOR, '[data-purpose="transcript-cue"]')

    for elem in transcript_elements:
        transcripts.append(elem.text)

    return "\n".join(transcripts)

def save_to_pdf(text, filename):
    """Saves transcript to PDF."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.output(filename)

if __name__ == "__main__":
    udemy_login()

    COURSE_URL = "https://www.udemy.com/course/machinelearning/learn/lecture/20091372#overview"
    transcript_text = get_transcripts(COURSE_URL)
    
    if transcript_text.strip():
        save_to_pdf(transcript_text, "udemy_transcript.pdf")
        print("✅ Transcript saved to udemy_transcript.pdf")
    else:
        print("⚠️ No transcript found!")

    driver.quit()
