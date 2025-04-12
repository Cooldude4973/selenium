from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from fpdf import FPDF

# Set up Selenium WebDriver
chrome_options = Options()
  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")

# service = Service("/path/to/chromedriver")  # Update with the actual path

# Launch the browser
driver = webdriver.Chrome()


def get_transcripts(course_url):
    driver.get(course_url)
    time.sleep(10)  # Allow page to load
    transcript_button = driver.find_elements(By.ID,"popper-trigger--549")
    if transcript_button:
        transcript_button[0].click()
        print("Transcript button clicked successfully!")
        time.sleep(5)
    else:
        pass
        time.sleep(5)
        element = driver.find_element(By.CSS_SELECTOR, '[data-purpose="go-to-next"]')
        if element:
            element.click()
        else:
            print("Both are not present")

    
    transcripts = []
    transcript_elements = driver.find_elements(By.CLASS_NAME, "transcript--cue-container--Vuwj6")
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

    COURSE_URL = "https://www.udemy.com/course/machinelearning/learn/lecture/20091372#overview"  # Replace with the actual course URL

    transcript_text = get_transcripts(COURSE_URL)
    save_to_pdf(transcript_text, "udemy_transcript.pdf")
    
    print("Transcript saved to udemy_transcript.pdf")
    driver.quit()
