import osimport pytestimport allurefrom common.contants import DATA_DIRfrom common.read_json import ReadJsonfrom common.handle_request import HandleRequestfrom common.handle_oracle import HandleDbfrom common.config import conffrom common.my_log import LoggerTEST_DATA_PLAN = os.path.join(DATA_DIR, "test_fdp_payment_revoke_osj116.json")logging = Logger(__name__).get_logger()@allure.feature('付款核销接口_OSJ116')@allure.testcase(conf.get("project_url", "url"), "测试地址：{}".format(conf.get("project_url", "url")))class TestRevokeOSJ116:    # 准备    json_object = ReadJson(TEST_DATA_PLAN)    json_datas = json_object.read_json()    cases = json_datas["cases"]    http = HandleRequest()    db = HandleDb()    @classmethod    def setup_class(self):        logging.info('------>执行前置操作,删除已存在的测试数据')        # 依次删除付款核销原始表、临时表、正式表中测试数据        self.db.del_data("DELETE  FROM FDP_AP_CHECK_CANCEL_TEMP  WHERE "                         "SOURCE_TRX_ID = '581559cd-031a-11ed-8db3-48d53963e04b'")        self.db.del_data("DELETE  FROM FDP_AP_CHECK_CANCEL_ORIGIN_TEMP  WHERE "                         "SOURCE_TRX_ID = '581559cd-031a-11ed-8db3-48d53963e04b'")        self.db.del_data("DELETE  FROM FDP_AP_CHECK_CANCEL_ORIGIN  WHERE "                         "SOURCE_TRX_ID = '581559cd-031a-11ed-8db3-48d53963e04b'")        self.db.del_data("DELETE  FROM FDP_AP_CHECK_CANCEL WHERE "                         "SOURCE_TRX_ID = '581559cd-031a-11ed-8db3-48d53963e04b'")    @classmethod    def teardown_class(self):        logging.info('------>执行后置操作,清理测试数据')        # 依次删除付款核销原始表、临时表、正式表中测试数据        self.db.del_data("DELETE  FROM FDP_AP_CHECK_CANCEL_TEMP  WHERE "                         "SOURCE_TRX_ID = '581559cd-031a-11ed-8db3-48d53963e04b'")        self.db.del_data("DELETE  FROM FDP_AP_CHECK_CANCEL_ORIGIN_TEMP  WHERE "                         "SOURCE_TRX_ID = '581559cd-031a-11ed-8db3-48d53963e04b'")        self.db.del_data("DELETE  FROM FDP_AP_CHECK_CANCEL_ORIGIN  WHERE "                         "SOURCE_TRX_ID = '581559cd-031a-11ed-8db3-48d53963e04b'")        self.db.del_data("DELETE  FROM FDP_AP_CHECK_CANCEL WHERE "                         "SOURCE_TRX_ID = '581559cd-031a-11ed-8db3-48d53963e04b'")        self.db.close()    @pytest.fixture()    # request.param：用于获取测试的请求参数    def case_data(self, request):        casedata = request.param        return casedata    @allure.title("测试业务类型OSJ116是否正确生成数据")    @allure.story('业务类型OSJ116测试用例')    @pytest.mark.parametrize('case_data', cases, indirect=True)    def test_revoke_OSJ116(self, case_data,base_headers):        with allure.step("准备OSJ116测试数据"):            url = conf.get("project_url", "url") + case_data["url"]            method = case_data["method"]            # 预期结果            expected = case_data["expected"]        # 调用付款核销接口，生成OSJ116数据        with allure.step("执行接口请求,生成OSJ116数据"):            response = self.http.send(url=url, method=method, json=case_data["json"],headers=base_headers)            result = response.json()        with allure.step("进行预期结果断言"):            try:                # 请求体断言                assert expected["code"] == result["code"]                assert expected["msg"] == result["msg"]                # 数据库断言--断言数据是否准确生成至库存调整数据同步正式表中                if case_data["check_sql_01"]:                    db_actul_results = list({db_actul_results for db_actul_results in                                                list(self.db.get_all(case_data["check_sql_01"]))})                try:                    assert db_actul_results[0][1] == case_data["json"]["sourceCode"]                    assert db_actul_results[0][2] == case_data["json"]["sourceTrxId"]                    assert db_actul_results[0][3] == case_data["json"]["sourceDocNumber"]                    assert db_actul_results[0][5] == '0'                    assert db_actul_results[0][6] == None                    assert db_actul_results[0][11] == case_data["json"]["companyCode"]                    logging.info('数据准确生成至付款核销明细表中,并且状态为0,数据为有效数据')                except KeyError as e:                    logging.info(f'数据未准确生成至付款核销明细表中：{e}')            except AssertionError as i:                logging.error("用例{}生成数据{}--执行失败!".format(case_data["title"], case_data["case_id"]))                logging.debug(                    "用例{}生成数据{}--失败请求参数：{}".format(case_data["title"], case_data["case_id"], case_data["json"]))                logging.error("用例{}生成数据{}--失败请求返回参数：{}".format(case_data["title"], case_data["case_id"], result))                logging.error("用例{}生成数据{}--报错信息：{}".format(case_data["title"], case_data["case_id"], i))                logging.debug("用例{}生成数据{}--预期结果：{}".format(case_data["title"], case_data["case_id"], expected))                raise i            else:                logging.info("用例OSJ116生成数据：{}-{}--执行通过".format(case_data["title"], case_data["case_id"]))if __name__ == '__main__':    self_test_OSJ116 = TestRevokeOSJ116()    self_test_OSJ116.test_revoke_OSJ116()