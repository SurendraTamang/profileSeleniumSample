import selenium
from selenium import webdriver
from lxml import html
import json

CHROME_DRIVER_PATH = 'chromedriver.exe'
USER_DATA_PATH = 'C:\\Users\\Vision\\AppData\\Local\\Google\\Chrome\\User Data'
def start_crawl():
    options = webdriver.ChromeOptions()
    options.add_argument(f'--user-data-dir={USER_DATA_PATH}')
    options.add_argument(f'--profile-directory=Profile 6')
    try:
        driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH,chrome_options=options)
        driver.get('https://jobs.smartrecruiters.com/oneclick-ui/company/AFRY/publication/7d385c8f-7082-4bd0-a7a9-940a8db6b125?dcr_id=DCRA1')

    except Exception as e:
        print("Error")
        print(e)
        driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
    
    #driver.get('https://jobs.smartrecruiters.com/oneclick-ui/company/AFRY/publication/7d385c8f-7082-4bd0-a7a9-940a8db6b125?dcr_id=DCRA1')
    driver.maximize_window()
    page = driver.page_source
    tree = html.fromstring(page)
    input_file = tree.xpath("//input")
    input_files = [{'field' : x.xpath('./@formcontrolname')[0],'required':x.xpath('./@aria-required')} for x in input_file if x.xpath('./@formcontrolname')]
    location = tree.xpath("//input[@aria-label='Location']/@aria-required")
    telephone  = tree.xpath("//input[@type='tel']/@aria-required")
    message = tree.xpath("//textarea[@id='hiring-manager-message-input']/@aria-required")
    required_files = {
    }
    for x in input_files:
        if x['required'] == ['true']:
            required_files[x['field']] = True
        else:
            required_files[x['field']] = False
    print(required_files)
    try:
        required_files['location'] = bool( location[0])
    except:
        required_files['location'] = False
    try:
        required_files['telephone'] = bool(telephone[0])


    except:
        required_files['telephone'] = False
    try:
        required_files['message'] = bool(message[0])
    except:
        required_files['message'] = False
    print(required_files)
    # output_json_file 
    with open('output_json_file.json', 'w') as outfile:
        json.dump(required_files, outfile, indent=3)

    return driver 


if __name__ == '__main__':
    start_crawl()