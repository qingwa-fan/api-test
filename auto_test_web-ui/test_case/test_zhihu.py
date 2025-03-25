from py_page.main_page import MainPage


class TestZhiHu:

    def test_click_MainPage_icon(self, base_driver):
        MainPage(base_driver).click_mainPage_icon()
