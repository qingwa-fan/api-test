import osimport pytestimport allurefrom common.contants import DATA_DIRfrom common.read_json import ReadJsonfrom common.handle_request import HandleRequestfrom common.handle_oracle import HandleDbfrom common.config import conffrom common.my_log import LoggerTEST_DATA_PLAN = os.path.join(DATA_DIR, "test_fdp_other_b2b152.json")logging = Logger(__name__).get_logger()@allure.feature('其他业务接口5-4_B2B152')@allure.testcase(conf.get("project_url", "url"), "测试地址：{}".format(conf.get("project_url", "url")))class TestOtherB2B152:    # 准备    json_object = ReadJson(TEST_DATA_PLAN)    json_datas = json_object.read_json()    cases = json_datas["cases"]    http = HandleRequest()    db = HandleDb()    @classmethod    def setup_class(self):        logging.info('------>执行前置操作,删除已存在的测试数据')        # 删除其他业务接口原始行表中数据        self.db.del_data("DELETE  FROM FDP_FIN_COMMON_LINE_TEMP WHERE HEADER_ID "                         "IN (SELECT HEADER_ID FROM FDP_FIN_COMMON_HEADER_TEMP WHERE "                         "SOURCE_TRX_ID LIKE 'B2B152_23061400%')")        # 删除其他业务接口原始头表中数据        self.db.del_data("DELETE FROM FDP_FIN_COMMON_HEADER_TEMP WHERE SOURCE_TRX_ID LIKE 'B2B152_23061400%'")        # 删除其他业务接口正式行表中数据        self.db.del_data("DELETE  FROM FDP_FIN_COMMON_LINE_T WHERE HEADER_ID "                         "IN (SELECT HEADER_ID FROM FDP_FIN_COMMON_HEADER_T WHERE "                         "SOURCE_TRX_ID LIKE 'B2B152_23061400%')")        # 删除其他业务接口正式头表中数据        self.db.del_data("DELETE FROM FDP_FIN_COMMON_HEADER_T WHERE SOURCE_TRX_ID LIKE 'B2B152_23061400%'")    @classmethod    def teardown_class(self):        logging.info('------>执行后置操作,清理测试数据')        # 删除其他业务接口原始行表中数据        self.db.del_data("DELETE  FROM FDP_FIN_COMMON_LINE_TEMP WHERE HEADER_ID "                         "IN (SELECT HEADER_ID FROM FDP_FIN_COMMON_HEADER_TEMP WHERE "                         "SOURCE_TRX_ID LIKE 'B2B152_23061400%')")        # 删除其他业务接口原始头表中数据        self.db.del_data("DELETE FROM FDP_FIN_COMMON_HEADER_TEMP WHERE SOURCE_TRX_ID LIKE 'B2B152_23061400%'")        # 删除其他业务接口正式行表中数据        self.db.del_data("DELETE  FROM FDP_FIN_COMMON_LINE_T WHERE HEADER_ID "                         "IN (SELECT HEADER_ID FROM FDP_FIN_COMMON_HEADER_T WHERE "                         "SOURCE_TRX_ID LIKE 'B2B152_23061400%')")        # 删除其他业务接口正式头表中数据        self.db.del_data("DELETE FROM FDP_FIN_COMMON_HEADER_T WHERE SOURCE_TRX_ID LIKE 'B2B152_23061400%'")        self.db.close()    @pytest.fixture()    # request.param：用于获取测试的请求参数    def case_data(self, request):        casedata = request.param        return casedata    @allure.title("测试业务类型B2B152是否正确生成数据，并且可以成功汇总且推送")    @allure.story('业务类型B2B152测试用例')    @pytest.mark.parametrize('case_data', cases, indirect=True)    def test_other_B2B152(self, case_data,base_headers):        with allure.step("准备B2B152测试数据"):            url = conf.get("project_url", "url") + case_data["url"]            method = case_data["method"]            # 预期结果            expected = case_data["expected"]        # 调用其他业务接口5-4，生成B2B152数据        with allure.step("执行接口请求,生成B2B152数据"):            response = self.http.send(url=url, method=method, json=case_data["json"],headers=base_headers)            result = response.json()        with allure.step("进行预期结果断言"):            try:                # 请求体断言                assert int(expected["code"]) == result["code"]                assert expected["msg"] == result["msg"]                assert expected["sourceCode"] == result["sourceCode"]                # 数据库断言--断言数据是否生成至其他业务接口原始表中，并且断言数据的准确性                if case_data["check_sql_01"]:                    if case_data["case_id"] == 'case_0':                        temp_actul_results = list({temp_actul_results for temp_actul_results in                                                self.db.get_all(case_data["check_sql_01"])})                        try:                            assert temp_actul_results[0][0] == temp_actul_results[0][1]                            assert temp_actul_results[0][2] == None                            assert temp_actul_results[0][3] == case_data["json"][0]["sourceTrxId"]                            assert temp_actul_results[0][4] == case_data["json"][0]["companyCode"]                            assert temp_actul_results[0][5] == temp_actul_results[0][7] == 1                            assert temp_actul_results[0][6] == case_data["json"][0]["trxTypeCode"]                            assert temp_actul_results[0][9] == int(case_data["json"][0]["lineRequestList"][0]["sourceLineId"])                            logging.info('数据成功生成至其他业务接口临时表中,数据为有效数据')                        except KeyError as e:                            logging.info(f'数据未生成至其他业务接口临时行表中：{e}')            except AssertionError as i:                logging.error("用例{}生成数据{}--执行失败!".format(case_data["title"], case_data["case_id"]))                logging.debug(                    "用例{}生成数据{}--失败请求参数：{}".format(case_data["title"], case_data["case_id"], case_data["json"]))                logging.error("用例{}生成数据{}--失败请求返回参数：{}".format(case_data["title"], case_data["case_id"], result))                logging.error("用例{}生成数据{}--报错信息：{}".format(case_data["title"], case_data["case_id"], i))                logging.debug("用例{}生成数据{}--预期结果：{}".format(case_data["title"], case_data["case_id"], expected))                raise i            else:                logging.info("用例B2B152生成数据：{}-{}--执行通过".format(case_data["title"], case_data["case_id"]))if __name__ == '__main__':    self_test_B2B152 = TestOtherB2B152()    self_test_B2B152.test_other_B2B152()