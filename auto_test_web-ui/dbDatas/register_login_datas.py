from dbDatas.ConnDB import ConnectDB


class RegisterLoginDatas:



    # 为测试用例提供根据tel查询用户数据
    def get_user_info_by_tel(self, mobile):
        sql = f"SELECT * FROM ls_user WHERE mobile = {mobile}"
        db = ConnectDB()
        res = db("select" ,sql)
        db(connect=False)
        return res

    # 为测试用例提供所有已注册的用户手机号
    def get_all_user_mobiles(self):
        sql="SELECT mobile FROM ls_user"
        db = ConnectDB()
        res = db("select", sql)
        mobiles_list = [mobile["mobile"] for mobile in res]
        db(connect=False)
        return mobiles_list     #['13111111', '19912312399'.....]



if __name__ == '__main__':
    db_data = RegisterLoginDatas()
    res = db_data.get_user_info_by_tel("13200000000")[0]
    re2 = db_data.get_all_user_mobiles()
    print(re2)