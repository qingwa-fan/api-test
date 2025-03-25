import osimport pytestimport allurefrom common.contants import DATA_DIRfrom common.read_json import ReadJsonfrom common.handle_request import HandleRequestfrom common.handle_oracle import HandleDbfrom common.config import conffrom common.my_log import LoggerTEST_DATA_PLAN = os.path.join(DATA_DIR, "test_fdp_other_osj108_osj109.json")logging = Logger(__name__).get_logger()@allure.feature('其他业务接口7_OSJ109')@allure.testcase(conf.get("project_url", "url"), "测试地址：{}".format(conf.get("project_url", "url")))class TestOtherOsj109:    # 准备    json_object = ReadJson(TEST_DATA_PLAN)    json_datas = json_object.read_json()    cases = json_datas["cases"]    http = HandleRequest()    db = HandleDb()    @classmethod    def setup_class(self):        logging.info('------>执行前置操作,删除已存在的测试数据')        # 删除应收事务临时表中OSJ108数据        self.db.del_data("DELETE  FROM XX_AR_TRX_DETAIL_TEMP  WHERE PURCHASE_ORDER_PRODUCT_ID = '230619001'")        # 删除应收事务明细表中OSJ108数据        self.db.del_data("DELETE  FROM XX_AR_TRX_DETAIL WHERE PURCHASE_ORDER_PRODUCT_ID = '230619001'")        # 删除冲减临时表中OSJ109数据        self.db.del_data("DELETE FROM XX_OFFSET_ESTIMATE_DETAIL_TEMP WHERE SOURCE_TRX_ID = 'OSJ109_test_230619001'")        # 删除冲减明细表中OSJ109数据        self.db.del_data("DELETE FROM XX_OFFSET_ESTIMATE_DETAIL WHERE SOURCE_TRX_ID = 'OSJ109_test_230619001'")    @classmethod    def teardown_class(self):        logging.info('------>执行后置操作,清理测试数据')        # 删除应收事务临时表中OSJ108数据        self.db.del_data("DELETE  FROM XX_AR_TRX_DETAIL_TEMP  WHERE PURCHASE_ORDER_PRODUCT_ID = '230619001'")        # 删除应收事务明细表中OSJ108数据        self.db.del_data("DELETE  FROM XX_AR_TRX_DETAIL WHERE PURCHASE_ORDER_PRODUCT_ID = '230619001'")        # 删除冲减临时表中OSJ109数据        self.db.del_data("DELETE FROM XX_OFFSET_ESTIMATE_DETAIL_TEMP WHERE SOURCE_TRX_ID = 'OSJ109_test_230619001'")        # 删除冲减明细表中OSJ109数据        self.db.del_data("DELETE FROM XX_OFFSET_ESTIMATE_DETAIL WHERE SOURCE_TRX_ID = 'OSJ109_test_230619001'")        self.db.close()    @pytest.fixture()    # request.param：用于获取测试的请求参数    def case_data(self, request):        casedata = request.param        return casedata    @allure.title("测试业务类型OSJ109是否正确生成数据")    @allure.story('业务类型OSJ109测试用例')    @pytest.mark.parametrize('case_data', cases, indirect=True)    def test_other_OSJ109(self, case_data,base_headers):        with allure.step("准备OSJ109测试数据"):            OSJ108_url = conf.get("project_url", "url") + case_data["OSJ108_url"]            OSJ109_url = conf.get("project_url", "url") + case_data["OSJ109_url"]            method = case_data["method"]            # 预期结果            OSJ108_expected = case_data["OSJ108_expected"]            OSJ109_expected = case_data["OSJ109_expected"]        # 调用其他业务接口7，生成B2B103数据        with allure.step("执行接口请求,生成OSJ108数据"):            response = self.http.send(url=OSJ108_url, method=method, json=case_data["OSJ108_json"],headers=base_headers)            OSJ108_result = response.json()            # result = response.text        with allure.step("执行接口请求,生成OSJ109数据"):            response = self.http.send(url=OSJ109_url, method=method, json=case_data["OSJ109_json"],headers=base_headers)            OSJ109_result = response.json()        with allure.step("进行预期结果断言"):            try:                # 请求体断言                assert OSJ108_expected["code"] == OSJ108_result["code"]                assert OSJ108_expected["msg"] == OSJ108_result["msg"]                assert OSJ109_expected["code"] == OSJ109_result["code"]                assert OSJ109_expected["msg"] == OSJ109_result["msg"]                logging.info('断言成功,返回信息正确')                # 数据库断言--判断应收明细表中,OSJ108与OSJ109的PURCHASE_ORDER_PRODUCT_ID、暂估id、company_code、往来单位存值是否一致                if case_data["check_sql_01"]:                    if case_data["case_id"] == 'case_0':                        db_actual_results = list({TEMP_actual_results for TEMP_actual_results in                                                  list(self.db.get_all(case_data["check_sql_01"]))})                        try:                            assert db_actual_results[0][0] == db_actual_results[0][1]\                                   == case_data["OSJ108_json"][0]["attribute4"] == case_data["OSJ109_json"][0]["attribute4"]                            assert db_actual_results[0][2] == db_actual_results[0][3] \                                   == case_data["OSJ108_json"][0]["country"] == case_data["OSJ109_json"][0]["country"]                            assert db_actual_results[0][4] == case_data["OSJ108_json"][0]["trxType"]                            assert db_actual_results[0][5] == case_data["OSJ109_json"][0]["trxType"]                            assert db_actual_results[0][6] == db_actual_results[0][7]\                                   == case_data["OSJ108_json"][0]["companyCode"] == case_data["OSJ109_json"][0]["companyCode"]                            assert db_actual_results[0][8] == db_actual_results[0][9]\                                   == case_data["OSJ108_json"][0]["customerNumber"] == case_data["OSJ109_json"][0]["customerNumber"]                            assert db_actual_results[0][10] == db_actual_results[0][11]\                                   == case_data["OSJ108_json"][0]["customerName"] == case_data["OSJ109_json"][0]["customerName"]                            assert db_actual_results[0][12] == int(case_data["OSJ108_json"][0]["lineAmount"])                            assert db_actual_results[0][13] == int(case_data["OSJ109_json"][0]["lineAmount"])                            assert db_actual_results[0][14] == db_actual_results[0][15] == 0                            logging.info('断言成功,数据成功生成至应收事务临时表中')                        except KeyError:                            logging.info('断言失败,数据生成错误')            except AssertionError as i:                logging.error("用例{}生成数据{}--执行失败!".format(case_data["title"], case_data["case_id"]))                logging.debug(                    "用例{}生成数据{}--失败请求参数：{}".format(case_data["title"], case_data["case_id"], case_data["OSJ109_json"]))                logging.error("用例{}生成数据{}--失败请求返回参数：{}".format(case_data["title"], case_data["case_id"], OSJ109_result))                logging.error("用例{}生成数据{}--报错信息：{}".format(case_data["title"], case_data["case_id"], i))                logging.debug("用例{}生成数据{}--预期结果：{}".format(case_data["title"], case_data["case_id"], OSJ109_expected))                raise i            else:                logging.info("用例OSJ109生成数据：{}-{}--执行通过".format(case_data["title"], case_data["case_id"]))if __name__ == '__main__':    self_test_OSJ109 = TestOtherOsj109()    self_test_OSJ109.test_other_OSJ109()