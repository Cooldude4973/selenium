from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fpdf import FPDF
import time

# Use Brave with an existing user profile
chrome_options = Options()
chrome_options.add_argument("--user-data-dir=C:\\Users\\Sahil Chalke\\AppData\\Local\\Google\\Chrome\\User Data")  # Change "YourUser"
chrome_options.add_argument("--profile-directory=Default")  # Use your existing Brave profile
chrome_options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(options=chrome_options)

def get_transcripts(course_url):
    driver.get(course_url)
    time.sleep(5)  # Allow page to load

    wait = WebDriverWait(driver, 10)

    try:
        transcript_button = wait.until(EC.element_to_be_clickable((By.ID, "popper-trigger--549")))
        transcript_button.click()
        print("Transcript button clicked successfully!")
        time.sleep(5)
    except:
        print("Transcript button not found. Trying 'Go to Next'.")

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, '[data-purpose="go-to-next"]')
            next_button.click()
        except:
            print("Neither transcript nor next button is present.")

    transcripts = []
    transcript_elements = driver.find_elements(By.CSS_SELECTOR, '[data-purpose="transcript-cue"]')

    for elem in transcript_elements:
        transcripts.append(elem.text)

    return "\n".join(transcripts)

def save_to_pdf(text, filename):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.output(filename)

if __name__ == "__main__":
    COURSE_URL = "https://www.udemy.com/course/machinelearning/learn/lecture/20091372#overview"

    transcript_text = get_transcripts(COURSE_URL)
    save_to_pdf(transcript_text, "udemy_transcript.pdf")

    print("Transcript saved to udemy_transcript.pdf")
    driver.quit()
