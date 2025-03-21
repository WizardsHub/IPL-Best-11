from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize WebDriver
driver = webdriver.Chrome()

# Open the IPL Stats website
url = "https://www.iplt20.com/stats/2024"
driver.get(url)

# Wait for page to fully load
time.sleep(10)  # Initial wait to ensure elements are rendered

wait = WebDriverWait(driver, 30)

# Locate and click the 'statstypefilter' dropdown
stat_filter = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'statstypefilter')]")))
driver.execute_script("arguments[0].scrollIntoView();", stat_filter)  # Scroll to element if needed
stat_filter.click()

# Continue with the rest of the script...

# Step 2: Select "Bowlers" from the dropdown
bowlers_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Bowlers')]")))
bowlers_option.click()
time.sleep(1)

# Step 3: Select "Purple Cap"
purple_cap_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Purple Cap')]")))
purple_cap_option.click()
time.sleep(2)  # Wait for table to load

# Step 4: Click on "View More" until all data loads
while True:
    try:
        view_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'View More')]")))
        view_more_button.click()
        time.sleep(2)  # Allow new rows to load
    except:
        break  # Exit loop when no more "View More" button is found

# Step 5: Scrape table data
rows = driver.find_elements(By.XPATH, "//table//tr")

data = []
for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    data.append([col.text for col in cols])

# Convert to DataFrame
df = pd.DataFrame(data, columns=["Position", "Player", "Matches", "Wickets", "Avg", "Econ", "SR", "4W", "5W"])

# Save data to CSV
df.to_csv("purple_cap_stats.csv", index=False)

# Close the driver
driver.quit()

print("Data successfully scraped and saved to 'purple_cap_stats.csv'.")