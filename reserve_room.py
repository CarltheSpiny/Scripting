from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date, timedelta, datetime
import time
import os
from selenium.webdriver.chrome.options import Options
import configparser

username = ""
password = ""
target_day = 0
target_month = 0
target_year = 0
target_date = 0
start = 0
end = 0
target_hour = 0
target_minute = 0
is_Config_Loaded = False

def date_fixer_upper():

    error_state = False
    
    target_day = date.today().day
    target_month = date.today().month
    target_year = date.today().year
    assumed_date = date.today() + timedelta(days=8)
    choice = str(input(f"This is today's date: {date.today()}, the target date is {assumed_date}. Is this correct? Y/N:"))

    if choice.lower() == "y" or choice == "":
        target_day = assumed_date.day
        target_month = assumed_date.month
        target_year = assumed_date.year
        target_date = f"{target_year}-{target_month}-{target_day}"

    else:
        target_month = int(input("Please enter the month: "))
        target_day = int(input("Please enter the day: "))
        target_year = int(input("Please enter the year: "))
        

        target_date = f"{target_year}-"

        if target_month < 10:
            target_date = target_date + f"0{target_month}-"
        else:
            target_date = target_date + f"{target_month}-"

        if target_day < 10:
            target_date = target_date + f"0{target_day}"
        else:
            target_date = target_date + f"{target_day}"

    while not error_state:
        print("Using the guide below, choose the room you would like to reserve:")
        print("5th Floor, Up to 9 People, Rm 5441 = 5441")
        print("5th Floor, Up to 9 People, Rm 5439 (HU Room) = 5439")
        print("4th Floor, Between 5-8 people, Rm 4136 = 4136")

        choice = input("Please enter the room code:")

        # 5th Floor, Up to 9 People, Rm 5441
        room_5441_page = f'https://cpp.libcal.com/r/accessible/availability?lid=8262&gid=14786&zone=5315&space=56426&capacity=3&date={target_date}'

        # 5th Floor, Up to 9 People, Rm 5439
        room_5439_page = f'https://cpp.libcal.com/r/accessible/availability?lid=8262&gid=14786&zone=5315&space=56425&capacity=3&date={target_date}'

        # 4th Floor, Between 5-8 people, Rm 4136
        room_4136_page = f'https://cpp.libcal.com/r/accessible/availability?lid=8262&gid=14785&zone=5317&space=56423&capacity=2&date={target_date}'

        if choice == "5441":
            return room_5441_page
        elif choice == "5439":
            return room_5439_page
        elif choice == "4136":
            return room_4136_page
        elif choice == "":
            return room_5441_page
        else:
            print("Incorrect room, please reselect a valid room")
            error_state = True
    
def my_CPP_Login_No_Duo(driver, username='miguelguzman', password='G00dFuture'):
    print("handling the login again")
    username_field_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username")), "Could not find username")

    if username_field_element:
        print("Found the username")

    password_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password")), "Could not find password")

    if password_element:
        print("Found the password")

    username_field_element.clear()
    username_field_element.send_keys(username)

    password_element.clear()
    password_element.send_keys(password)

    login_button_xPath = '//*[@id="formcontainer"]/form/button'

    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
        By.XPATH, login_button_xPath)), "Could not find login button")
    
    login_button.send_keys(Keys.ENTER)
    while "Library" not in driver.title:
        print("waiting on screen to load...")

    print("Finished handling login again")

def libraryCrawl(link, start = 1, end = 2, driver=webdriver.Chrome):
    driver.get(link)
    
    for i in range(start, end + 1):
        try:

            label_xPath = f'/html/body/div[2]/main/div/div/div/div[1]/div/form/div/div[1]/div[2]/fieldset/div[{i}]/label'
            checkbox_fullXpath = f'/html/body/div[2]/main/div/div/div/div[1]/div/form/div/div[1]/div[2]/fieldset/div[{i}]/label/input'
            
            checkbox = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,  checkbox_fullXpath)), "could not find checkbox")
            
            label = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, label_xPath))
            )

            if checkbox and label:
                print(f"found the check_box: {i}")

            if checkbox.send_keys(Keys.SPACE):
                print(f"clicked the checkbox: {i}")

            if checkbox.is_selected:
                print("Confirmed selection")

        except Exception as e:
            print(f"Couldnt find a checkox, maybe it wasn't available anymore or there aren't enough boxes: {e}")
    
    submit_button_xPath = '/html/body/div[2]/main/div/div/div/div[1]/div/form/div/div[2]/button'


    submit_button = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.XPATH, submit_button_xPath)), "could not find clickable button")
    
    if submit_button:
        print("Found submit button")
        
        if submit_button.is_enabled:
            print("button is enabled")
            submit_button.send_keys(Keys.SPACE)
            print('Clicked button')

            if "Library" not in driver.title:
                # <-------------- clicking this button prompts the user to sign in again ------------>
                #my_CPP_Login_No_Duo(driver)
                pass
            
            print("finding continue...")
            continue_button_xPath = '//*[@id="terms_accept"]'
            continue_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
                By.XPATH, continue_button_xPath)), "Could not find continue")
            
            if continue_button:
                print("found conitnue button")
                if continue_button.click:
                    print("clicked continue button")
                    continue_button.send_keys(Keys.ENTER)
            else:
                print("could not find continue button")

            submit_booking_button_xPath = '//*[@id="btn-form-submit"]'
            submit_booking_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, submit_booking_button_xPath)), "Could not find submit booking")
            
            if submit_booking_button.send_keys(Keys.SPACE):
                input("Waiting on input...")
            
        else:
            print("button is not enabled yet")

def timedExecute(link, driver):
    # 14 + 1 30 minute slots, from 7:30am to 9:00pm
    print("1: 7:30am to 8am | 2: 8am to 8:30am | 3: 8:30am to 9am | 4: 9am to 9:30am | 5: 9:30am to 10am | 6: 10am to 10:30am")
    print("7: 10:30am to 11am | 8: 11am to 11:30am | 9: 11:30am to 12pm | 10: 12pm to 12:30pm | 11: 12:30pm to 1pm | 12: 1pm to 1:30pm")
    print("13: 1:30pm to 2pm | 14: 2pm to 2:30pm | 15: 2:30pm to 3pm | 16: 3pm to 3:30pm | 17: 3:30pm to 4pm")

    print("Special Codes: 30: 9am to 3pm | 40: 10am to 4pm")
    start = 0
    end = 0

    start = int(input("Enter the starting index for the start time: "))

    if start == 30:
        start = 4
        end = 15
    elif start == 40:
        start = 6
        end = 17

    else:
        end = int(input("Enter the ending index for the end time: "))

    # 9-3 pm Tuesday-Thursday
    # 10-4 pm Mondays

    target_hour = 0
    target_minute = 0
    choice = input(f"This script will visit the site {link} and reserve the room automatically. Would you like to wait till 11:59 p.m? (Select no for manual time input) (y/n): ")
    
    if choice == "n":
        print("Input these times in military time. ( 1pm = 13, 2pm = 14, etc.)")
        target_hour = int(input("Hours?"))
        target_minute = int(input("Minutes?"))

    else:
        target_hour = 23
        target_minute = 59

    print(f"Will start script at {target_hour}:{target_minute}")
    while True:
        # Get the current time
        now = datetime.now()
        
        # Check if the time matches 11:59 PM
        if now.hour == target_hour and now.minute == target_minute:
            print("It's time! Executing the block of code...")
            libraryCrawl(link, start, end, driver)
            # Break the loop or continue as needed
            input("Successfully reserved the room. Press any key to exit....")
            driver.quit()
            break
        
        # Sleep for a while before checking the time again (e.g., 30 seconds)
        time.sleep(5)

def my_CPP_Login(link, username='miguelguzman', password='G00dFuture', driver=webdriver.Chrome()):
    username_field_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )

    if username_field_element:
        print("Found the username")

    password_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    )

    if password_element:
        print("Found the password")

    username_field_element.clear()
    username_field_element.send_keys(username)
    driver.implicitly_wait(10)

    password_element.clear()
    password_element.send_keys(password)
    driver.implicitly_wait(10)

    login_button_xPath = '//*[@id="formcontainer"]/form/button'
    '''login_button_element = WebDriverWait(driver, 600).until(
        EC.presence_of_element_located((By.XPATH, login_button_xPath))
    )'''

    login_button = WebDriverWait(driver, 300).until(EC.element_to_be_clickable((
        By.XPATH, login_button_xPath)))
    login_button.send_keys(Keys.ENTER)

    driver.implicitly_wait(30)
    other_options_link_xPath = '//*[@id="auth-view-wrapper"]/div[2]/div[6]/a'
    duo_link_element = driver.find_element(By.XPATH, other_options_link_xPath)

    if duo_link_element:
        print("Found duo link")
        duo_trust_device_xPath = '//*[@id="trust-browser-button"]'
        trust_device_element = driver.find_element(By.XPATH, duo_trust_device_xPath)

        if trust_device_element:
            print("found trust devices button")
            trust_device_element.send_keys(Keys.SPACE)

        while "Home" not in driver.title:
            my_cpp_name_link = '//*[@id="portlet_u31l1n9"]/h1/a/img'
            my_cpp_name_element = driver.find_element(By.XPATH, my_cpp_name_link)
            
            if my_cpp_name_element:
                print("found the myCPP page")
                timedExecute(link, driver)
        else:
            print("finished waiting on duo and reached myCPP Home page")

def main():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    filename = 'messages.html'
    file_path = os.path.join(current_directory, filename)

    '''load_config = input("Do you want to load the conifg file?: (Y/N)")

    if load_config.lower == "y":
        # Initialize the config parser
        config = configparser.ConfigParser()

        # Read the INI file
        config.read("config.ini")

        # Access the data
        username = config["User"]["username"]         # Load string (name)
        password = config["User"]["password"]         # Load string (name)
        target_day = int(config["User"]["day"])      # Load integer (age)
        target_month = int(config["User"]["month"])
        target_year = int(config["User"]["year"])
        target_date = int(config["User"]["date"])
        start = int(config["User"]["start"])
        end = int(config["User"]["end"])
        target_hour = int(config["User"]["hour"])
        target_minute = int(config["User"]["minute"])
        is_Config_Loaded = True'''
    
    chrome_options = Options()
    chrome_options.add_argument("--log-level=3")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f"file:///{file_path}")

    input("This script will reserve a room. You will be prompted to login with to myCPP wit Duo to get your credentials, then you will be taken to the study room page. \nYou will need to manually click the duo login button and select 'Yes' when asked to remember this device. \nPress any button to continue...")
    use_defaults = False

    username = input("Please enter your myCPP username:")
    if username == "":
        print("no username, using default (Miguel's)")
        use_defaults = True
    password = input("Please enter your myCPP password:")
    if password == "":
        print("no password given, using default (Miguel's)")
        use_defaults = True

    room_link = date_fixer_upper()

    
    myCPP_link = 'https://my.cpp.edu/'
    driver.get(myCPP_link)

    assert "CPP Signon" in driver.title

    if use_defaults:
        my_CPP_Login(room_link, driver=driver)
    else:
        my_CPP_Login(room_link, username, password, driver=driver)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An Error occured: {e}")