from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from webdriver_manager.chrome import ChromeDriverManager


target_year = 2024
target_day = 17
target_month = 10

target_date = f"{target_year}-"

if target_month < 10:
    target_date = target_date + f"0{target_month}-"
else:
    target_date = target_date + f"{target_month}-"

if target_day < 10:
    target_date = target_date + f"0{target_day}"
else:
    target_date = target_date + f"{target_day}"

# 5th Floor, Up to 9 People, Rm 5441
room_5441_page = f'https://cpp.libcal.com/r/accessible/availability?lid=8262&gid=14786&zone=5315&space=56426&capacity=3&date={target_date}'

# 5th Floor, Up to 9 People, Rm 5439
room_5439_page = f'https://cpp.libcal.com/r/accessible/availability?lid=8262&gid=14786&zone=5315&space=56425&capacity=3&date={target_date}'

# 4th Floor, Between 5-8 people, Rm 4136
room_4136_page = f'https://cpp.libcal.com/r/accessible/availability?lid=8262&gid=14785&zone=5317&space=56423&capacity=2&date={target_date}'

#cookie for login
cookie = '001c09903a21d9812622fa61e5e2738605215c03d5185c8f5786e05de8e0eb06f6773986b8191ffacb2724822a6f465968034201c88b8081b6bde1a9e068490154987b69940ad4f3cdf0c3b90b0cdd5e1e2e87f5b50d1006158e0caf1446593037e1b32ee9c93a2869494af7910f872f7a7b34c332c0b3e433e477d9a6b8c44bf078acbebf2a313fd6f5e32c46c5092df74e45e0845cb3b6a87631c8c80a5d87fdefd656f358c5091cad9b3ebb4cb25f2899cb9ce'

# Base search for screen reader
search_for_room_page = 'https://cpp.libcal.com/r/accessible'

next_page_button_loc = '//*[@id="eq-time-grid"]/div[1]/div[1]/div/button[2]'
dummy_date = '//*[@id="eq-time-grid"]/div[2]/div/table/tbody/tr/td[3]/div/div/div/table/tbody/tr/td/div/div[2]/div[1]'
select_times_dropdown = '//*[@id="bookingend_1"]'

# Options for the driver
options = Options()
options.add_argument("start-maximized")
# options.headless = True (toggle to enable guis)

driver = webdriver.Chrome(options=options)
print(f"Going to the following page:{room_5439_page}")
driver.get(room_5439_page)
# driver.add_cookie(cookie_dict={'name': 'lc_ea_po', 'value': cookie})

checkbox_id = 1


for i in range(1, 3):
    try:
        checkbox_fullXpath = f'/html/body/div[2]/main/div/div/div/div[1]/div/form/div/div[1]/div[2]/fieldset/div[{i}]/label/input'
        checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,  checkbox_fullXpath)))

        if checkbox:
            print(f"found the check_box: {i}")

        if checkbox.click:
            print(f"clicked the checkbox: {i}")
    except Exception:
        print("Couldnt find a checkox, maybe it wasn't available anymore?")

submit_button = None
altXPath = '//*[@id="s-lc-submit-times"]'
base = '/html/body/div[2]/main/div/div/div/div[1]/div/form/div/div[2]/button'
id = 's-lc-submit-times'

find_button = driver.find_element(By.XPATH, base)

if find_button:
    print("found button via find_element")

if find_button.click:
    print('Clicked the find button')

    WebDriverWait(driver, 30).until(EC.url_changes(room_5439_page), "page did not change")

    new_button_xpath = '//*[@id="username"]'
    try:
        new_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, new_button_xpath)), "Could not find this element")
        if new_button:
            print("found button on a new page")

    except Exception as e:
        print(f"Caught an Exception: {e}, Ending page: {driver.current_url}")


print("Ending page: ", driver.current_url)

'''#Button getters and setters
next_page_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, next_page_button_loc))
)

if next_page_button.click:
    print("Clicked the next calander page")

date_item = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, dummy_date))
)

if date_item.click:
    print("Clicked the date item")

select_menu = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, select_times_dropdown))
)

if select_menu:
    print("found the select menu")'''


# print(driver.page_source)