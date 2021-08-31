from checkDriver import driver


def tennis_login(username, password):
    driver.get("https://auth.fft.fr/auth/realms/master/protocol/openid-connect/"
               "auth?client_id=FED_MET&response_type=code&scope=openid&redirect_uri=https://"
               "tenup.fft.fr/user-auth/process")

    driver.find_element_by_id("username").send_keys(username)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_xpath("//*[@id='kc-form']/div[3]/button").click()
    driver.implicitly_wait(2)   # on peut aussi attendre un temps déterminé avec : sleep(2)
    driver.find_element_by_class_name("menu-name").click()
    driver.find_element_by_xpath('//*[@id="page-header"]/div[2]/div/nav/ul/li[5]/div/div/ul/li[3]/ul/li[4]/a').click()
    result = driver.find_element_by_xpath('//*[@id="block-system-main"]/div/div/div/div[1]').text
    return result
