import osimport pytestimport allurefrom common.contants import DATA_DIRfrom common.read_json import ReadJsonfrom common.handle_request import HandleRequestfrom common.handle_oracle import HandleDbfrom common.config import conffrom common.my_log import LoggerTEST_DATA_PLAN = os.path.join(DATA_DIR, "test_fdp_other_osj123.json")logging = Logger(__name__).get_logger()@allure.feature('其他业务接口5-5_OSJ123')@allure.testcase(conf.get("project_url", "url"), "测试地址：{}".format(conf.get("project_url", "url")))class TestOtherOSJ123:    # 准备    json_object = ReadJson(TEST_DATA_PLAN)    json_datas = json_object.read_json()    cases = json_datas["cases"]    http = HandleRequest()    db = HandleDb()    @classmethod    def setup_class(self):        logging.info('------>执行前置操作,删除已存在的测试数据')        # 删除应付冲减暂估明细临时表中数据        self.db.del_data("DELETE FROM FDP_AP_OFF_ESTIMATE_DETAIL_TEMP WHERE  SOURCE_TRX_ID = 'OSJ123_23062001'")        # 删除应付冲减暂估明细明细表中数据        self.db.del_data("DELETE FROM FDP_AP_OFF_ESTIMATE_DETAIL WHERE  SOURCE_TRX_ID = 'OSJ123_23062001'")        # 删除其他业务接口正式行表中数据        self.db.del_data("DELETE  FROM FDP_FIN_COMMON_LINE_T WHERE HEADER_ID "                         "IN (SELECT HEADER_ID FROM FDP_FIN_COMMON_HEADER_T WHERE "                         "SOURCE_TRX_ID ='OSJ123_23062001')")        # 删除其他业务接口正式头表中数据        self.db.del_data("DELETE FROM FDP_FIN_COMMON_HEADER_T WHERE SOURCE_TRX_ID ='OSJ123_23062001'")    @classmethod    def teardown_class(self):        logging.info('------>执行后置操作,清理测试数据')        # 删除应付冲减暂估明细临时表中数据        self.db.del_data("DELETE FROM FDP_AP_OFF_ESTIMATE_DETAIL_TEMP WHERE  SOURCE_TRX_ID = 'OSJ123_23062001'")        # 删除应付冲减暂估明细明细表中数据        self.db.del_data("DELETE FROM FDP_AP_OFF_ESTIMATE_DETAIL WHERE  SOURCE_TRX_ID = 'OSJ123_23062001'")        # 删除其他业务接口正式行表中数据        self.db.del_data("DELETE  FROM FDP_FIN_COMMON_LINE_T WHERE HEADER_ID "                         "IN (SELECT HEADER_ID FROM FDP_FIN_COMMON_HEADER_T WHERE "                         "SOURCE_TRX_ID ='OSJ123_23062001')")        # 删除其他业务接口正式头表中数据        self.db.del_data("DELETE FROM FDP_FIN_COMMON_HEADER_T WHERE SOURCE_TRX_ID ='OSJ123_23062001'")        self.db.close()    @pytest.fixture()    # request.param：用于获取测试的请求参数    def case_data(self, request):        casedata = request.param        return casedata    @allure.title("测试业务类型OSJ123是否正确生成数据，并且可以成功汇总且推送")    @allure.story('业务类型OSJ123测试用例')    @pytest.mark.parametrize('case_data', cases, indirect=True)    def test_other_OSJ123(self, case_data,base_headers):        with allure.step("准备OSJ123测试数据"):            url = conf.get("project_url", "url") + case_data["url"]            method = case_data["method"]            # 预期结果            expected = case_data["expected"]        # 调用其他业务接口5-5，生成OSJ123数据        with allure.step("执行接口请求,生成OSJ123数据"):            response = self.http.send(url=url, method=method, json=case_data["json"],headers=base_headers)            result = response.json()        with allure.step("进行预期结果断言"):            try:                # 请求体断言                assert expected["code"] == result["code"]                assert expected["msg"] == result["msg"]                # 数据库断言--断言数据是否准确生成应付冲减暂估明细正式表                if case_data["check_sql_01"]:                    db_actul_results = list({db_actul_results for db_actul_results in                                                list(self.db.get_all(case_data["check_sql_01"]))})                    print(db_actul_results)                try:                    assert db_actul_results[0][0] == case_data["json"][0]["sourceCode"]                    assert db_actul_results[0][1] == case_data["json"][0]["sourceTrxId"]                    assert db_actul_results[0][2] == case_data["json"][0]["sourceDocNumber"]                    assert db_actul_results[0][3] == case_data["json"][0]["companyCode"]                    assert db_actul_results[0][4] == case_data["json"][0]["country"]                    assert db_actul_results[0][5] == case_data["json"][0]["trxTypeCode"]                    assert db_actul_results[0][6] == case_data["json"][0]["currencyCode"]                    assert db_actul_results[0][7] == case_data["json"][0]["skuCode"]                    assert db_actul_results[0][8] == case_data["json"][0]["vendorNum"]                    assert db_actul_results[0][9] == case_data["json"][0]["vendorName"]                    assert db_actul_results[0][10] == int(case_data["json"][0]["qty"])                    assert db_actul_results[0][11] == float(case_data["json"][0]["lineAmount"])                    assert db_actul_results[0][12] == 0                    assert db_actul_results[0][13] == case_data["json"][0]["taxCategory"]                    assert db_actul_results[0][14] == case_data["json"][0]["taxCode"]                    assert db_actul_results[0][15] == int(case_data["json"][0]["taxAmount"])                    logging.info('数据成功生成至其他业务接口明细表中,并且状态为0,数据为有效数据')                except KeyError as e:                    logging.info(f'数据未生成至其他业务接口明细表中：{e}')            except AssertionError as i:                logging.error("用例{}生成数据{}--执行失败!".format(case_data["title"], case_data["case_id"]))                logging.debug(                    "用例{}生成数据{}--失败请求参数：{}".format(case_data["title"], case_data["case_id"], case_data["json"]))                logging.error("用例{}生成数据{}--失败请求返回参数：{}".format(case_data["title"], case_data["case_id"], result))                logging.error("用例{}生成数据{}--报错信息：{}".format(case_data["title"], case_data["case_id"], i))                logging.debug("用例{}生成数据{}--预期结果：{}".format(case_data["title"], case_data["case_id"], expected))                raise i            else:                logging.info("用例OSJ123生成数据：{}-{}--执行通过".format(case_data["title"], case_data["case_id"]))if __name__ == '__main__':    self_test_OSJ123 = TestOtherOSJ123()    self_test_OSJ123.test_other_OSJ123()