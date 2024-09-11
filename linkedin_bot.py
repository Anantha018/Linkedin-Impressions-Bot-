import time
import selenium.webdriver as WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

CONNECTIONS_PAGE = "https://www.linkedin.com/search/results/people/"
HOME_PAGE = "https://www.linkedin.com/feed/"
my_connection_profiles_urls = []
temp_profiles_urls = []
all_profiles_urls = []

class LinkedInBot:
    def __init__(self):
        self.driver = None
        options = WebDriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222") 
        self.driver = WebDriver.Chrome(options=options)
        
    def get_profiles(self):
        return WebDriverWait(self.driver, 120).until(
            EC.presence_of_all_elements_located((By.XPATH, ".//span[@class='entity-result__title-line entity-result__title-line--2-lines ']//a[@class='app-aware-link ' and @href]"))
        )
    
    def iterate_all_the_user_connected_profiles_urls(self):
        first_degree_connections_button = WebDriverWait(self.driver, 120).until(
                EC.presence_of_element_located((By.XPATH, ".//button[@aria-label='1st']"))
            )
        
        if first_degree_connections_button.is_displayed():
            self.driver.execute_script("window.scrollBy(0, 800);")
            # time.sleep(3)
            self.driver.execute_script("window.scrollBy(0, -800);")
            all_profiles = self.get_profiles()
            
            for profile in all_profiles:
                profile_url = profile.get_attribute('href')
                if profile_url not in my_connection_profiles_urls:
                    my_connection_profiles_urls.append(profile_url)
    
    def iterate_all_the_profiles_urls(self):
        third_degree_button = WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, ".//button[@aria-label='3rd+']"))
        )
        
        if third_degree_button.is_displayed():
            self.driver.execute_script("window.scrollBy(0, 800);")
            # time.sleep(3)
            self.driver.execute_script("window.scrollBy(0, -800);")
            all_profiles = self.get_profiles()
            
            for profile in all_profiles:
                temp_profiles_urls.append(profile.get_attribute('href'))
            
    def search_user_entered_job_titles(self, titles_and_counts):
        try:

            for title, profiles_count in titles_and_counts.items():
                self.driver.get(HOME_PAGE)
                search_box = WebDriverWait(self.driver, 120).until(
                    EC.presence_of_element_located((By.XPATH, ".//input[@aria-label='Search']"))
                )
                
                temp_profiles_urls.clear()  # Clear before each search
                
                search_box.clear()
                search_box.send_keys(f"{title} people")
                time.sleep(2)
                search_box.send_keys(Keys.ENTER)
                time.sleep(2)
                
                try:
                    no_results_found_page = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, ".//section//h2[contains(@class,'ember-view artdeco-empty-state__headline artdeco-empty-state')]"))
                    )
                    if no_results_found_page.is_displayed():
                        print(f"No results found for: {title}")
                        continue
                
                except TimeoutException:
                    # Apply the third-degree filter
                    filter_third_people = WebDriverWait(self.driver, 120).until(
                        EC.presence_of_element_located((By.XPATH, "(.//a[@class='app-aware-link  artdeco-pill artdeco-pill--slate artdeco-pill--choice artdeco-pill--2 reusable-search__entity-cluster--quick-filter-action'])[3]"))
                    )
                    filter_third_people.click()
                    
                    third_degree_button = WebDriverWait(self.driver, 120).until(
                        EC.presence_of_element_located((By.XPATH, ".//button[@aria-label='3rd+']"))
                    )
                    
                    if third_degree_button.is_displayed():
                        current_profile_count = 0
                        while current_profile_count < profiles_count:
                            self.iterate_all_the_profiles_urls()
                            all_profiles_urls.extend(temp_profiles_urls)  # Add profiles to the main list
                            
                            # Scroll to the bottom to make sure the "Next" button is visible
                            self.driver.execute_script("window.scrollBy(0, 800);")

                            # Try to find and click the "Next" button
                            try:
                                next_page = WebDriverWait(self.driver, 15).until(
                                    EC.element_to_be_clickable((By.XPATH, ".//button[@aria-label='Next']"))
                                )
                                next_page.click()
                                current_profile_count += len(temp_profiles_urls)
                                temp_profiles_urls.clear()  # Clear after each page
                            except TimeoutException as e:
                                print("Next button not found or another error:", str(e))
                                break
            
            all_unique_profiles_urls = set()

            for item in all_profiles_urls:
                if item not in all_unique_profiles_urls:
                    all_profiles_urls.append(item)
                    all_unique_profiles_urls.add(item)
            self.go_to_profiles(all_unique_profiles_urls)  # Process all profiles collected
                
        except Exception as e:
            print("An error occurred:", str(e))
  
    def go_to_profiles(self, connection_profiles):
        for profile in connection_profiles:
            try:
                self.driver.get(profile)  # Navigate to the profile URL
                time.sleep(3)             # Wait for 3 seconds on the profile page
            except Exception as e:
                print(f"An error occurred while processing {profile}: {str(e)}")
        
        self.quit()
    
    def iterate_through_pages(self):
        try:
            while True:
                # Iterate through profiles on the current page
                self.iterate_all_the_user_connected_profiles_urls()

                # Scroll to the bottom to make sure the "Next" button is visible
                self.driver.execute_script("window.scrollBy(0, 800);")

                # Try to find and click the "Next" button
                try:
                    next_page = WebDriverWait(self.driver, 15).until(
                        EC.element_to_be_clickable((By.XPATH, ".//button[@aria-label='Next']"))
                    )
                    next_page.click()
                    
                except TimeoutException:
                    print("Reached the last page or 'Next' button not found.")
                    for i in my_connection_profiles_urls:
                        print(i)
                    print(len(my_connection_profiles_urls))
                    self.go_to_profiles(my_connection_profiles_urls)
                    break  # Exit the loop when there is no "Next" button

        except Exception as e:
            print("An error occurred:", str(e))
         
    def go_to_connections_page(self):
        self.driver.get(CONNECTIONS_PAGE)
        try:
            try:
                no_results_found_page = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, ".//section//h2[contains(@class,'ember-view artdeco-empty-state__headline artdeco-empty-state')]"))
                )
                if no_results_found_page.is_displayed():
                   return 
            except:
                first_degree_connections_button = WebDriverWait(self.driver, 120).until(
                    EC.presence_of_element_located((By.XPATH, ".//button[@aria-label='1st']"))
                )
                first_degree_connections_button.click()
                
                self.iterate_through_pages()
            
        except TimeoutException as e:
            print("Element not found or timeout occurred:", str(e))

    def quit(self):
        try:
            # Quit the WebDriver and close the browser window
            self.driver.quit()
            # A message box after this
        except Exception as e:
            print(f"An error occurred while trying to quit the driver: {e}")
              
if __name__ == "__main__":
    pass
    # bot = LinkedInBot()
    # bot.go_to_connections_page()
    # titles_and_counts = {
    # "software engineer": 10,
    # "data scientist": 20
    # }
    # bot.search_user_entered_job_titles(titles_and_counts)

# For windows = "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\chrome-profile"
#or --> & "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\chrome-profile"
# In terminal or powershell 

# For MAC os = /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222&
# #!/bin/bash