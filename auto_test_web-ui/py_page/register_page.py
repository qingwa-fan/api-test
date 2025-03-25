from py_page.base_page import BasePage


class RegisterPage(BasePage):

    path = BasePage.get_path("/py_yaml/register_page.yaml")

    def user_register(self, mobile, password):
        self.run_steps(self.path,"user_register", mobile=mobile, password=password)
        return self

    def get_register_tosta_text(self):
        res = self.run_steps(self.path, "get_register_tosta_text")
        return res.text
