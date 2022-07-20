import time
from selenium import webdriver
import base64
import re

"""

this program scrape edukasystem's rangkuman
the scrape target is in image file

"""

#convert BLOB data to base64 image data
def get_file_content_chrome(browser, uri):
  result = browser.execute_async_script("""
    var uri = arguments[0];
    var callback = arguments[1];
    var toBase64 = function(buffer){for(var r,n=new Uint8Array(buffer),t=n.length,a=new Uint8Array(4*Math.ceil(t/3)),i=new Uint8Array(64),o=0,c=0;64>c;++c)i[c]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charCodeAt(c);for(c=0;t-t%3>c;c+=3,o+=4)r=n[c]<<16|n[c+1]<<8|n[c+2],a[o]=i[r>>18],a[o+1]=i[r>>12&63],a[o+2]=i[r>>6&63],a[o+3]=i[63&r];return t%3===1?(r=n[t-1],a[o]=i[r>>2],a[o+1]=i[r<<4&63],a[o+2]=61,a[o+3]=61):t%3===2&&(r=(n[t-2]<<8)+n[t-1],a[o]=i[r>>10],a[o+1]=i[r>>4&63],a[o+2]=i[r<<2&63],a[o+3]=61),new TextDecoder("ascii").decode(a)};
    var xhr = new XMLHttpRequest();
    xhr.responseType = 'arraybuffer';
    xhr.onload = function(){ callback(toBase64(xhr.response)) };
    xhr.onerror = function(){ callback(xhr.status) };
    xhr.open('GET', uri);
    xhr.send();
    """, uri)
  if type(result) == int :
    raise Exception("Request failed with status %s" % result)
  return base64.b64decode(result)

#handle rangkuman page
#rangkuman page contains the BLOB image file
def scr_rangkuman(bab,num_subbab,smstr_num,mapel):
    attempt = 0
    title = ""

    while 1:

        try:
            title_container = browser.find_element_by_xpath("//div[@class='index_content__header_3UyOF']/p").text
            title = title_container
            img_container = browser.find_element_by_xpath("//div[@class='content-pinch-zoom']/div/img")
            break
    
        except Exception as exc:
            if attempt >=5:
                print(mapel + "//" +"Semester" + str(smstr_num) + " - " +bab + " - " +str(num_subbab)+ " "+ title + " SKIPPED")
                browser.back()
                browser.back()
                time.sleep(10)
                return None
            
            print("Image is loading...")
            attempt+=1
            time.sleep(1)
    
    url = img_container.get_attribute("src")

    #convert blob to base64 image
    bytes = get_file_content_chrome(browser, url)
    title = re.sub('[^a-zA-Z0-9 \n\.]', '', title.replace("(","").replace(")",""))
    with open( mapel + "//" +"Semester" + str(smstr_num) + " - " +bab + " - " +str(num_subbab)+ " "+ title+".png", "wb") as fh:
        fh.write(bytes)
    
    #back/previous page
    print(bab + " " + str(num_subbab) + " has been sucessfully downloaded"  )
    browser.back()
    browser.back()

    time.sleep(10)



def scr_semester(smstr_num,mapel):
    time.sleep(5)
    container = "//div[@class='unlocked-chapter-list-container']"

    for i in range(1,100):
        current_bab = container + "/div["+ str(i) +"]"
        try:    
            for j in range(1,100):
                
                    if i > 1:
                        browser.find_element_by_xpath(current_bab).click()
                    subbab_container = current_bab + "/div/div[2]/div"
                    browser.find_element_by_xpath(subbab_container)
                    bab_name = browser.find_element_by_xpath(container + "/div["+ str(i) +"]" + "/div/div/div[1]").text
                
                    item = subbab_container + "/div[" + str(j) + "]"

                    try:

                        time.sleep(5)
                        button_item = browser.find_element_by_xpath(item + "/div/button[text()=' Rangkuman ']")
                        button_item.click()

                        time.sleep(5)

                        scr_rangkuman(bab_name,j,smstr_num,mapel)

                    except Exception as exc:
                        print(exc)
                        print("BAB " + str(i) + " SUBBAB " + str(j) + " did not found" ) 
                        time.sleep(5)
                        break
        except Exception as exc:
            print("BAB " + str(i) + " did not found" )
            break

#browser Options
options = webdriver.ChromeOptions()
options.binary_location = 'B:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--disable-notifications")
chrome_driver_binary = "B:\\driver\\chromedriver.exe"
browser = webdriver.Chrome(chrome_driver_binary, chrome_options=options)

#open browser
browser.get("https://login.edukasystem.com/auth/login")

time.sleep(15)

#get login form
input_username = browser.find_element_by_xpath("//div[@class='index_login__field__container_2odbD']/div[1]/div/input")
input_password = browser.find_element_by_xpath("//div[@class='index_login__field__container_2odbD']/div[2]/div/input")

#fill login info
input_username.send_keys("username")
input_password.send_keys("password")

#Press LogIn Button
browser.find_element_by_xpath("//section[@class='index_login__action__container_hbke6']/button").click()
time.sleep(10)


container_mapel = "//div[@class='course-section-container']" #div(1-13)

for i in range(1,14):
    
    xpath_mapel = container_mapel + "/div[" + str(i) + "]"

    #semester range (1 - 6)
    for j in range(1,7):
        
        browser.get("https://www.edukasystem.com/bank-soal-list")
        time.sleep(10)

        semester_button = browser.find_element_by_xpath(xpath_mapel + "/div/div/div[" + str(j) + "]")
        mapel_name_text = browser.find_element_by_xpath(xpath_mapel + "/header/p").text
        semester_button.click()
        scr_semester(j,mapel_name_text)        