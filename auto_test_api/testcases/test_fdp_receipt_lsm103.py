import osimport pytestimport allurefrom common.contants import DATA_DIRfrom common.read_json import ReadJsonfrom common.handle_request import HandleRequestfrom common.handle_oracle import HandleDbfrom common.config import conffrom common.my_log import LoggerTEST_DATA_PLAN = os.path.join(DATA_DIR, "test_fdp_receipt_lsm103.json")logging = Logger(__name__).get_logger()@allure.feature('应收收款接口_LSM103')@allure.testcase(conf.get("project_url", "url"), "测试地址：{}".format(conf.get("project_url", "url")))class TestReceiptLSM103:    # 准备    json_object = ReadJson(TEST_DATA_PLAN)    json_datas = json_object.read_json()    cases = json_datas["cases"]    http = HandleRequest()    db = HandleDb()    @classmethod    def setup_class(self):        logging.info('------>执行前置操作,删除已存在的测试数据')        # 删除应收收款原始临时表中数据        self.db.del_data("DELETE  FROM XX_AR_RECEIPT_DETAIL_TEMP RT  WHERE SOURCE_TRX_ID = 'LSM103_20230627002'")        # 删除应收收款临时表中数据        self.db.del_data("DELETE FROM XX_AR_RECEIPT_DETAIL RT  WHERE SOURCE_TRX_ID = 'LSM103_20230627002'")        # 删除应收收款正式表中数据        self.db.del_data("DELETE   FROM FDP_AR_RECEIPT  WHERE SOURCE_TRX_ID = 'LSM103_20230627002'")    @classmethod    def teardown_class(self):        logging.info('------>执行后置操作,清理测试数据')        # 删除应收收款原始临时表中数据        self.db.del_data("DELETE  FROM XX_AR_RECEIPT_DETAIL_TEMP RT  WHERE SOURCE_TRX_ID = 'LSM103_20230627002'")        # 删除应收收款临时表中数据        self.db.del_data("DELETE FROM XX_AR_RECEIPT_DETAIL RT  WHERE SOURCE_TRX_ID = 'LSM103_20230627002'")        # 删除应收收款正式表中数据        self.db.del_data("DELETE   FROM FDP_AR_RECEIPT  WHERE SOURCE_TRX_ID = 'LSM103_20230627002'")        self.db.close()    @pytest.fixture()    # request.param：用于获取测试的请求参数    def case_data(self, request):        casedata = request.param        return casedata    @allure.title("测试业务类型LSM103是否正确生成数据，并且可以成功汇总且推送")    @allure.story('业务类型LSM103测试用例')    @pytest.mark.parametrize('case_data', cases, indirect=True)    def test_receipt_LSM103(self, case_data, base_headers):        with allure.step("准备LSM103测试数据"):            url = conf.get("project_url", "url") + case_data["url"]            method = case_data["method"]            # 预期结果            expected = case_data["expected"]        # 调用应收收款接口，生成LSM103数据        with allure.step("执行接口请求,生成LSM103数据"):            response = self.http.send(url=url, method=method, json=case_data["json"], headers=base_headers)            result = response.json()        with allure.step("进行预期结果断言"):            try:                # 请求体断言                assert expected["code"] == result["code"]                assert expected["msg"] == result["msg"]                # 数据库断言--断言数据是否生成至应付发票原始临时表中，判断头表header_id是否等于行表header_id、行总金额是否等于头总金额、以及状态                if case_data["check_sql_01"]:                    temp_actul_results = list({temp_actul_results for temp_actul_results in                                               list(self.db.get_all(case_data["check_sql_01"]))})                    print(temp_actul_results)                try:                    assert temp_actul_results[0][0] == case_data["json"][0]["sourceTrxId"]                    assert temp_actul_results[0][1] == case_data["json"][0]["companyCode"]                    assert temp_actul_results[0][2] == case_data["json"][0]["receiptMethodName"]                    assert temp_actul_results[0][3] == case_data["json"][0]["customerId"]                    assert str(temp_actul_results[0][4]) == case_data["json"][0]["bankAccountId"]                    assert str(temp_actul_results[0][5]) == case_data["json"][0]["trxAmount"]                    logging.info('数据成功生成至应收收款原始临时表,并且状态为S,数据为有效数据')                except KeyError as e:                    logging.info(f'数据未生成至应收收款原始临时表中：{e}')                # 数据库断言--断言数据是否生成至其他业务接口明细表中，判断头表header_id是否等于行表header_id、行总金额是否等于头总金额、以及状态                if case_data["check_sql_02"]:                    origin_actul_results = list({origin_actul_results for origin_actul_results in                                                 list(self.db.get_all(case_data["check_sql_02"]))})                    print(origin_actul_results[0][4])                    print(case_data["json"][0]["bankAccountId"])                try:                    assert origin_actul_results[0][0] == case_data["json"][0]["sourceTrxId"]                    assert origin_actul_results[0][1] == case_data["json"][0]["companyCode"]                    assert origin_actul_results[0][2] == case_data["json"][0]["receiptMethodName"]                    assert origin_actul_results[0][3] == case_data["json"][0]["customerId"]                    assert str(origin_actul_results[0][4]) == case_data["json"][0]["bankAccountId"]                    assert str(origin_actul_results[0][5]) == case_data["json"][0]["trxAmount"]                    logging.info('数据成功生成至应收收款临时表,并且状态为S,数据为有效数据')                except KeyError as e:                    logging.info(f'数据未生成至应收收款临时表中：{e}')            except AssertionError as i:                logging.error("用例{}生成数据{}--执行失败!".format(case_data["title"], case_data["case_id"]))                logging.debug(                    "用例{}生成数据{}--失败请求参数：{}".format(case_data["title"], case_data["case_id"],                                                               case_data["json"]))                logging.error(                    "用例{}生成数据{}--失败请求返回参数：{}".format(case_data["title"], case_data["case_id"], result))                logging.error("用例{}生成数据{}--报错信息：{}".format(case_data["title"], case_data["case_id"], i))                logging.debug(                    "用例{}生成数据{}--预期结果：{}".format(case_data["title"], case_data["case_id"], expected))                raise i            else:                logging.info("用例LSM103生成数据：{}-{}--执行通过".format(case_data["title"], case_data["case_id"]))if __name__ == '__main__':    self_test_LSM103 = TestReceiptLSM103()    self_test_LSM103.test_receipt_LSM103()