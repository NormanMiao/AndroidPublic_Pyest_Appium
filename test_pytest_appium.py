# -*- coding: UTF-8 -*-
# coding=utf-8
import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
import os
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
app_package ="com.tencent.wetestdemo"
app_activity = "com.tencent.wetestdemo.LoginActivity"


class TestWetestDemo():
    driver = None

    @classmethod
    def setup_class(cls):
        # 定义一个字典，存储capability信息
        desired_caps = {
            "platformName": "Android",
            "appPackage": "com.tencent.wetestdemo",
            "appActivity": "com.tencent.wetestdemo.LoginActivity"
        }
        cls.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)
        cls.wait = WebDriverWait(cls.driver, 10, 0.5)

    #@classmethod
    #def teardown_class(cls):
        #cls.driver.stop_client()
        #print("结束测试")

    #def setup(self):
        #print("启动app")
        #self.driver.start_activity(app_package, app_activity)
        #time.sleep(5)

    #def teardown(self):
        #print("停止app")
        #self.driver.close_app()


    def test_login_fail(self):
        """不输入账号密码，直接登录——出现Login Failed的弹窗"""
        # 判断登录按钮存在


        locate=(By.ID,'com.tencent.wetestdemo:id/login')
        # 点击登录
        self.wait.until(EC.visibility_of_element_located(locate)).click()
        print("登录失败")
        time.sleep(5)
        # 弹窗出现
        locate=(By.XPATH,'//android.widget.Button[@text="OK"]')
        fail_msg = self.wait.until(EC.visibility_of_element_located(locate))
        fail_msg.click()
        assert fail_msg is not None

    def test_login_success(self):
        """输入账号密码——登录成功——进入SELECT页面——断言左上角SELECT元素存在"""
        # 输入账号
        locate = (By.ID, "com.tencent.wetestdemo:id/username")
        self.wait.until(EC.visibility_of_element_located(locate)).send_keys("norman")
        # 输入密码
        locate = (By.ID,"com.tencent.wetestdemo:id/password")
        self.wait.until(EC.visibility_of_element_located(locate)).send_keys("123456")

        # 点击登录
        locate = (By.ID, "com.tencent.wetestdemo:id/login")
        self.wait.until(EC.visibility_of_element_located(locate)).click()
        # 进入勾选页，判断submit按钮存在
        locate = (By.ID, "com.tencent.wetestdemo:id/submitbtn")
        submit = self.wait.until(EC.visibility_of_element_located(locate))
        assert submit is not None


    def test_check_elements(self):
        """登录——勾选item0,item5，点击提交，进入check页，检查内容为item0和item5"""
        # 登录，进入SELECT页
        self.test_login_success()
        # 选中item0
        locate = (By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.'
                                                      'view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.'
                                                      'widget.CheckedTextView[1]')
        self.wait.until(EC.visibility_of_element_located(locate)).click()
        '''item_0 = self.driver.find_element(by=AppiumBy.XPATH,
                                                value='/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.'
                                                      'view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.'
                                                      'widget.CheckedTextView[1]')'''

        # 选中item5
        locate = (By.XPATH,'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.'
                                                'view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ListView/android.'
                                                'widget.CheckedTextView[6 ]')
        self.wait.until(EC.visibility_of_element_located(locate)).click()
        # 点击提交

        locate = (By.ID, "com.tencent.wetestdemo:id/submitbtn")
        self.wait.until(EC.visibility_of_element_located(locate)).click()
        # 进入check页，检查内容为item0和item5（上一页勾选的内容）
        locate = (By.XPATH, '//android.widget.TextView[@text="[Item0, Item5]"]')
        item_check =  self.wait.until(EC.visibility_of_element_located(locate))
        assert item_check is not None
        print("checked")

