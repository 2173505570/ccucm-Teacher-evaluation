# -*- coding = utf-8 -*-
# @Time :4/7/2023 下午1:11
# @Author hai
# @File : 教评4.0.py
# @Software: PyCharm
import os
import selenium
import sys
import pickle
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep

def save_account_info(username, password):
    with open("account_info.pkl", "wb") as f:
        account_info = {"username": username, "password": password}
        pickle.dump(account_info, f)

def load_account_info():
    try:
        with open("account_info.pkl", "rb") as f:
            account_info = pickle.load(f)
            return account_info["username"], account_info["password"]
    except FileNotFoundError:
        return None, None
print('□□□□□■□□□□□□□□□□□■□□□□□□□■□□□□□□■□□□□□□□□■□□□□□□□□□□□□□□□□□□□□□\n'
'□□■■■■■■□□□□□□■■■■■■□□□□□■□□□□□■■□□□□□■■■■■■□□□□■■□□□□□■■□□□\n'
'□■■■■□■■■□□□□■■■■□■■■□□□□■□□□□□■■□□□□■■■■□■■■□□□■■■□□□■■■□□□\n'
'□■■□□□□■■□□□□■■□□□□■■□□□□■□□□□□■■□□□□■■□□□□■■□□□■■■□□□■■■□□□\n'
'■■■□□□□□□□□□■■■□□□□□□□□□□■□□□□□■■□□□■■■□□□□□□□□□■■■■□□■■■□□□\n'
'■■□□□□□□□□□□■■□□□□□□□□□□□■□□□□□■■□□□■■□□□□□□□□□□■■■■□■■□■□□□\n'
'■■■□□□□□■□□□■■■□□□□□■□□□□■■□□□□■■□□□■■■□□□□□■□□□■■■■□■■□■□□□\n'
'□■■□□□□■■■□□□■■□□□□■■■□□□■■□□□□■■□□□□■■□□□□■■■□□■■□■■■□□■□□□\n'
'□■■■■□■■■□□□□■■■■□■■■□□□□■■■■■■■■□□□□■■■■□■■■□□□■■□■■■□□■□□□\n'
'□□■■■■■■□□□□□□■■■■■■□□□□□□■■■■■■□□□□□□■■■■■■□□□□■■□■■■□□■□□□\n'
'□□□□■■□□□□□□□□□□■■□□□□□□□□□□□□□□□□□□□□□□■■□□□□□□□□□□□□□□□□□□\n')
print('---------------------欢迎使用ccucm自动教评软件-----------------------------')
print('---------------------本软件开源免费，严禁贩卖商用-----------------------------')
print('---------------------本软件是模拟人工点击的方式完成不会对账号有任何影响----------')
print('---------------------若出现软件不能运行请重启软件---------------------------')
print('---------------------使用前请先食用使用教程.docx---------------------------')
print('---------------------还在努力学习中，软件不是很好用请见谅！！！--------------')
print('---------------------有什么更好的想法请联系我QQ2173505570-----------------')
print('---------------------当浏览器弹出后不需要进行任何操作----------------------')
print('-----有时候会因为网络原因浏览器无操作，请手动关闭浏览器和软件后重启本软件---------')
while True:
    print("请选择登录方式(输入完后按回车键确认):")
    print("1. 使用上次保存的账号登录（若第一次使用请按2）" )
    print("2. 输入新账号登录" )
    choice = input("请输入选项（1或2）: ")

    if choice == "1":
        username, password = load_account_info()
        if not username or not password:
            print("未找到保存的账号信息，请选择输入新账号登录。")
            continue
    elif choice == "2":
        while True:
            try:
                username = int(input('请输入账号（学号）(输入完后按回车键确认): '))
                password = input('请输入密码（含大小写）(输入完后按回车键确认): ')
                break
            except ValueError:
                print('账号必须为整数数字，请检查后重试')
        save_account_info(username, password)
    else:
        print("无效选项，请重新选择。")
        continue
    break


# Rest of your code...
driver = webdriver.Edge()
url = 'http://jwxt.ccucm.edu.cn:8080/login.aspx'
driver.get(url)
sleep(3)
cob_role = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'cobRole'))
)

cob_role.click()

dropdown_menu = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, 'cobRole_DDD_PW-1'))
)

options = dropdown_menu.find_elements(By.TAG_NAME, 'td')

for option in options:
    if option.text == '学生':
        option.click()
        break

element = driver.find_element(By.ID, 'User_ID')
element.send_keys(username)

element = driver.find_element(By.ID, 'User_Pass')
element.send_keys(password)

# 定位验证码输入框和验证码文本
code_input = driver.find_element(By.ID, "txtVolidate")
code_text = driver.find_element(By.ID, "v_container").text

# 解析验证码文本并计算验证码答案
code_list = code_text.split(" ")
code_answer = str(int(code_list[0]) + int(code_list[2]))  # 8 + 16 = ?

# 将验证码答案填入验证码输入框
code_input.send_keys(code_answer)
driver.find_element(By.ID, 'Button1').click()
sleep(5)
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "li.btn a[href='TCStudent/SStudentEvaluateTeacher.aspx'][target='navTab']"))
)
element.click()
sleep(2)

# 转化到iframe页面
iframe = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="navTab"]/div[2]/div[2]/iframe'))
)
driver.switch_to.frame(iframe)
# 跳过进入提示页面
driver.find_element(By.ID, 'CBDeclare').click()
sleep(1)
driver.find_element(By.ID, 'BtnOK_CD').click()
sleep(2)

# 跳出循环后进行评教完成操作
max_iterations = 50
for i in range(max_iterations):
    wait = WebDriverWait(driver, 10, 0.5)
    elements = wait.until(
        EC.visibility_of_all_elements_located((By.XPATH, "//input[@type='radio']"))
    )
    clicked = False  # 追踪是否有 radio 标签被点击过
    # 检查 radio 标签是否有被点击的情况
    is_clicked = False
    for radio_button in elements:
        if radio_button.is_selected():
            is_clicked = True
            break

    # 如果有被点击的 radio 标签，则跳出循环
    if is_clicked:
        driver.quit()
        print('教评已完成将在5s后退出')
        sleep(5)
        sys.exit()
    for radio_button in elements:
        element = radio_button.find_element(By.XPATH, '..//label')
        text = element.text

        if '优秀' in text:
            radio_button.click()

            elements = driver.find_elements(By.XPATH, '//input[@name="radioSatisfaction"]')

            for radio_button in elements:
                if '非常称职' in radio_button.get_attribute('value'):
                    radio_button.click()
                    break

    driver.find_element(By.ID, "txtSuggest").send_keys('无' + Keys.TAB)
    sleep(3)
    driver.find_element(By.ID, "btnSave_CD").click()
    sleep(5)

    # # 完成评教后退出循环
    # driver.quit()
    # print('已完成将在5s后退出')
    # sleep(5)
    # sys.exit()
    # driver.find_element(By.ID,"txtSuggest").send_keys('无' + Keys.TAB)
    # sleep(3)
    # driver.find_element(By.ID,"btnSave_CD").click()
    # sleep(5)


