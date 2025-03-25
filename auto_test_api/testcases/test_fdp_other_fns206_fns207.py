import osimport pytestimport allurefrom common.contants import DATA_DIRfrom common.read_json import ReadJsonfrom common.handle_request import HandleRequestfrom common.handle_oracle import HandleDbfrom common.config import conffrom common.my_log import LoggerTEST_DATA_PLAN = os.path.join(DATA_DIR, "test_fdp_other_fns206_fns207.json")print(TEST_DATA_PLAN)logging = Logger(__name__).get_logger()@allure.feature('其他业务接口3_FNS206_FNS207')@allure.testcase(conf.get("project_url", "url"), "测试地址：{}".format(conf.get("project_url", "url")))class TestOtherFNS207:    # 准备    json_object = ReadJson(TEST_DATA_PLAN)    json_datas = json_object.read_json()    cases = json_datas["cases"]    http = HandleRequest()    db = HandleDb()    @classmethod    def setup_class(self):        logging.info('------>执行前置操作,删除已存在的测试数据')        # 删除FNS206的数据        # 删除其他业务接口临时行表中数据        self.db.del_data("DELETE  FROM FDP_FIN_COMMON_LINE_TEMP WHERE HEADER_ID "                         "IN (SELECT HEADER_ID FROM FDP_FIN_COMMON_HEADER_TEMP WHERE "                         "SOURCE_TRX_ID ='FNS206-20230621001')")        # 删除其他业务接口临时头表中数据        self.db.del_data(            "DELETE FROM FDP_FIN_COMMON_HEADER_TEMP WHERE SOURCE_TRX_ID ='FNS206-20230621001'")        # 删除其他业务接口正式行表中数据        self.db.del_data("DELETE  FROM FDP_FIN_COMMON_LINE_T WHERE HEADER_ID "                         "IN (SELECT HEADER_ID FROM FDP_FIN_COMMON_HEADER_T WHERE "                         "SOURCE_TRX_ID ='FNS206-20230621001')")        # 删除其他业务接口正式头表中数据        self.db.del_data(            "DELETE FROM FDP_FIN_COMMON_HEADER_T WHERE SOURCE_TRX_ID ='FNS206-20230621001'")        # 删除FNS207的数据        # 删除其他业务接口原始行表中数据        self.db.del_data("DELETE  FROM FDP_FIN_COMMON_LINE_TEMP WHERE HEADER_ID "                         "IN (SELECT HEADER_ID FROM FDP_FIN_COMMON_HEADER_TEMP WHERE "                         "SOURCE_TRX_ID ='FNS207-20230621001')")        # 删除其他业务接口原始头表中数据        self.db.del_data(            "DELETE FROM FDP_FIN_COMMON_HEADER_TEMP WHERE SOURCE_TRX_ID ='FNS207-20230621001'")        # 删除其他业务接口正式行表中数据        self.db.del_data("DELETE  FROM FDP_FIN_COMMON_LINE_T WHERE HEADER_ID "                         "IN (SELECT HEADER_ID FROM FDP_FIN_COMMON_HEADER_T WHERE "                         "SOURCE_TRX_ID ='FNS207-20230621001')")        # 删除其他业务接口正式头表中数据        self.db.del_data(            "DELETE FROM FDP_FIN_COMMON_HEADER_T WHERE SOURCE_TRX_ID ='FNS207-20230621001'")    @classmethod    def teardown_class(self):        logging.info('------>执行后置操作,清理测试数据')        # 删除FNS206的数据        # 删除其他业务接口原始行表中数据        self.db.del_data("DELETE  FROM FDP_FIN_COMMON_LINE_TEMP WHERE HEADER_ID "                         "IN (SELECT HEADER_ID FROM FDP_FIN_COMMON_HEADER_TEMP WHERE "                         "SOURCE_TRX_ID ='FNS206-20230621001')")        # 删除其他业务接口原始头表中数据        self.db.del_data(            "DELETE FROM FDP_FIN_COMMON_HEADER_TEMP WHERE SOURCE_TRX_ID ='FNS206-20230621001'")        # 删除其他业务接口正式行表中数据        self.db.del_data("DELETE  FROM FDP_FIN_COMMON_LINE_T WHERE HEADER_ID "                         "IN (SELECT HEADER_ID FROM FDP_FIN_COMMON_HEADER_T WHERE "                         "SOURCE_TRX_ID ='FNS206-20230621001')")        # 删除其他业务接口正式头表中数据        self.db.del_data(            "DELETE FROM FDP_FIN_COMMON_HEADER_T WHERE SOURCE_TRX_ID ='FNS206-20230621001'")        # 删除FNS207的数据        # 删除其他业务接口原始行表中数据        self.db.del_data("DELETE  FROM FDP_FIN_COMMON_LINE_TEMP WHERE HEADER_ID "                         "IN (SELECT HEADER_ID FROM FDP_FIN_COMMON_HEADER_TEMP WHERE "                         "SOURCE_TRX_ID ='FNS207-20230621001')")        # 删除其他业务接口原始头表中数据        self.db.del_data(            "DELETE FROM FDP_FIN_COMMON_HEADER_TEMP WHERE SOURCE_TRX_ID ='FNS207-20230621001'")        # 删除其他业务接口正式行表中数据        self.db.del_data("DELETE  FROM FDP_FIN_COMMON_LINE_T WHERE HEADER_ID "                         "IN (SELECT HEADER_ID FROM FDP_FIN_COMMON_HEADER_T WHERE "                         "SOURCE_TRX_ID ='FNS207-20230621001')")        # 删除其他业务接口正式头表中数据        self.db.del_data(            "DELETE FROM FDP_FIN_COMMON_HEADER_T WHERE SOURCE_TRX_ID ='FNS207-20230621001'")        self.db.close()    @pytest.fixture()    # request.param：用于获取测试的请求参数    def case_data(self, request):        casedata = request.param        print(casedata)        return casedata    @allure.title("测试业务类型FNS207是否正确生成数据")    @allure.story('业务类型FNS207测试用例')    @pytest.mark.parametrize('case_data', cases, indirect=True)    def test_other_FNS207(self, case_data,base_headers):        with allure.step("准备FNS207测试数据"):            FNS206_url = conf.get("project_url", "url") + case_data["FNS206_url"]            FNS207_url = conf.get("project_url", "url") + case_data["FNS207_url"]            method = case_data["method"]            # 预期结果            FNS206_expected = case_data["FNS206_expected"]            FNS207_expected = case_data["FNS207_expected"]        # 调用其他业务接口，生成FNS206数据        with allure.step("执行接口请求,生成FNS206数据"):            response = self.http.send(url=FNS206_url, method=method, json=case_data["FNS206_json"],headers=base_headers)            FNS206_result = response.json()            print(FNS206_result)            # result = response.text        with allure.step("执行接口请求,生成FNS207数据"):            response = self.http.send(url=FNS207_url, method=method, json=case_data["FNS207_json"],headers=base_headers)            FNS207_result = response.json()            print(FNS207_result)        with allure.step("进行预期结果断言"):            try:                # 请求体断言                assert FNS206_expected["code"] == FNS206_result["code"]                assert FNS206_expected["msg"] == FNS206_result["msg"]                assert FNS207_expected["code"] == FNS207_result["code"]                assert FNS207_expected["msg"] == FNS207_result["msg"]                logging.info('断言成功,返回信息正确')                # 数据库断言--判断其他业务接口表,FNS206数据是否准确                if case_data["check_sql_01"]:                    if case_data["case_id"] == 'case_0':                        db_actual_results = list({db_actual_results for db_actual_results in                                                  list(self.db.get_all(case_data["check_sql_01"]))})                        # print(db_actual_results)                        try:                            assert db_actual_results[0][0] == case_data["FNS206_json"]["trxAmount"]                            assert db_actual_results[0][1] == case_data["FNS206_json"]["sourceTrxId"]                            # assert db_actual_results[0][2] == case_data["B2B133_json"][0]["companyCode"]                            # assert db_actual_results[0][3] == case_data["B2B133_json"][0]["trxType"]                            # assert db_actual_results[0][4] == case_data["B2B133_json"][0]["customerId"]                            # assert db_actual_results[0][5] == case_data["B2B133_json"][0]["customerNum"]                            # assert db_actual_results[0][6] == case_data["B2B133_json"][0]["customerName"]                            # assert db_actual_results[0][7] == int(case_data["B2B133_json"][0]["bankAccountId"])                            # assert db_actual_results[0][8] == case_data["B2B133_json"][0]["bankAccountName"]                            # assert db_actual_results[0][9] == int(case_data["B2B133_json"][0]["receiptAmount"])                            # assert db_actual_results[0][10] == 0                            logging.info('数据成功生成至其他业务接口行表、头表中,并且状态为S,数据为有效数据')                        except KeyError:                            logging.info('断言失败,数据生成错误')                # 数据库断言--判断跨币种收款明细表中,FNS207数据是否准确                if case_data["check_sql_02"]:                    if case_data["case_id"] == 'case_0':                        db_actual_results_02 = list({db_actual_results_02 for db_actual_results_02 in                                                  list(self.db.get_all(case_data["check_sql_02"]))})                        print(db_actual_results_02)                        try:                            assert db_actual_results_02[0][0] == case_data["FNS207_json"]["trxAmount"]                            assert db_actual_results_02[0][1] == case_data["FNS207_json"]["sourceTrxId"]                            # assert db_actual_results_02[0][2] == case_data["B2B161_json"][0]["sourceDocNumber"]                            # assert db_actual_results_02[0][3] == case_data["B2B161_json"][0]["receiptSourceTrxId"]                            # assert db_actual_results_02[0][4] == None                            # assert db_actual_results_02[0][5] == case_data["B2B161_json"][0]["companyCode"]                            # assert db_actual_results_02[0][6] == case_data["B2B161_json"][0]["country"]                            # assert db_actual_results_02[0][7] == case_data["B2B161_json"][0]["trxTypeCode"]                            # assert db_actual_results_02[0][8] == case_data["B2B161_json"][0]["customerId"]                            # assert db_actual_results_02[0][9] == case_data["B2B161_json"][0]["exchangeRate"]                            # assert db_actual_results_02[0][10] == case_data["B2B161_json"][0]["receiptAccountName"]                            # assert db_actual_results_02[0][11] == case_data["B2B161_json"][0]["receiptAccountId"]                            # assert db_actual_results_02[0][12] == int(case_data["B2B161_json"][0]["trxAmount"])                            # assert db_actual_results_02[0][13] == case_data["B2B161_json"][0]["currencyCode"]                            logging.info('数据成功生成至其他业务接口行表、头表中,并且状态为S,数据为有效数据')                        except KeyError:                            logging.info('断言失败，测试不通过')            except AssertionError as i:                logging.error("用例{}生成数据{}--执行失败!".format(case_data["title"], case_data["case_id"]))                logging.debug(                    "用例{}生成数据{}--失败请求参数：{}".format(case_data["title"], case_data["case_id"], case_data["FNS207_json"]))                logging.error("用例{}生成数据{}--失败请求返回参数：{}".format(case_data["title"], case_data["case_id"], FNS207_result))                logging.error("用例{}生成数据{}--报错信息：{}".format(case_data["title"], case_data["case_id"], i))                logging.debug("用例{}生成数据{}--预期结果：{}".format(case_data["title"], case_data["case_id"], FNS207_expected))                raise i            else:                logging.info("用例FNS207生成数据：{}-{}--执行通过".format(case_data["title"], case_data["case_id"]))if __name__ == '__main__':    self_test_FNS207 = TestOtherFNS207()    self_test_FNS207.test_other_FNS207()