import osimport pytestimport allurefrom common.contants import DATA_DIRfrom common.read_json import ReadJsonfrom common.handle_request import HandleRequestfrom common.handle_oracle import HandleDbfrom common.config import conffrom common.my_log import LoggerTEST_DATA_PLAN = os.path.join(DATA_DIR, "test_fdp_invoices_lgs115.json")logging = Logger(__name__).get_logger()@allure.feature('应付发票接口_LGS115')@allure.testcase(conf.get("project_url", "url"), "测试地址：{}".format(conf.get("project_url", "url")))class TestReceivableLGS115:    # 准备    json_object = ReadJson(TEST_DATA_PLAN)    json_datas = json_object.read_json()    cases = json_datas["cases"]    http = HandleRequest()    db = HandleDb()    @classmethod    def setup_class(self):        logging.info('------>执行前置操作,删除已存在的测试数据')        # 删除应付发票临时头表中数据        self.db.del_data("DELETE  FROM FDP_AP_INVOICE_HEADER_ORIGIN_TEMP WHERE "                         "SOURCE_TRX_ID LIKE 'LGS115_2306210%'")        # 删除应付发票临时行表中数据        self.db.del_data("DELETE   FROM FDP_AP_INVOICE_LINE_ORIGIN_TEMP  WHERE "                         "SOURCE_LINE_ID LIKE '23062100%'")        # 删除应付发票原始头表中数据        self.db.del_data("DELETE  FROM FDP_AP_INVOICE_HEADER_ORIGIN WHERE  "                         "SOURCE_TRX_ID LIKE 'LGS115_2306210%'")        # 删除应付发票原始行表中数据        self.db.del_data("DELETE  FROM FDP_AP_INVOICE_LINE_ORIGIN  WHERE "                         "SOURCE_LINE_ID  LIKE '23062100%' ")    @classmethod    def teardown_class(self):        logging.info('------>执行后置操作,清理测试数据')        # 删除应付发票临时头表中数据        self.db.del_data("DELETE  FROM FDP_AP_INVOICE_HEADER_ORIGIN_TEMP WHERE "                         "SOURCE_TRX_ID LIKE 'LGS115_2306210%'")        # 删除应付发票临时行表中数据        self.db.del_data("DELETE   FROM FDP_AP_INVOICE_LINE_ORIGIN_TEMP  WHERE "                         "SOURCE_LINE_ID LIKE '23062100%'")        # 删除应付发票原始头表中数据        self.db.del_data("DELETE  FROM FDP_AP_INVOICE_HEADER_ORIGIN WHERE  "                         "SOURCE_TRX_ID LIKE 'LGS115_2306210%'")        # 删除应付发票原始行表中数据        self.db.del_data("DELETE  FROM FDP_AP_INVOICE_LINE_ORIGIN  WHERE "                         "SOURCE_LINE_ID  LIKE '23062100%' ")        self.db.close()    @pytest.fixture()    # request.param：用于获取测试的请求参数    def case_data(self, request):        casedata = request.param        return casedata    @allure.title("测试业务类型LGS115是否正确生成数据")    @allure.story('业务类型LGS115测试用例')    @pytest.mark.parametrize('case_data', cases, indirect=True)    def test_receivable_LGS115(self, case_data,base_headers):        with allure.step("准备LGS115测试数据"):            url = conf.get("project_url", "url") + case_data["url"]            method = case_data["method"]            # 预期结果            expected = case_data["expected"]        # 调用应付发票接口，生成LGS115数据        with allure.step("执行接口请求,生成LGS115数据"):            response = self.http.send(url=url, method=method, json=case_data["json"], headers=base_headers)            result = response.json()        with allure.step("进行预期结果断言"):            try:                # 请求体断言                assert expected["code"] == result["code"]                assert expected["msg"] in result["msg"]                logging.info('断言成功,返回信息正确')                # 数据库断言--断言数据是否生成至应付发票临时表中，判断SOURCE_TRX_ID、行表status、头表status,以及行金额、税金额                if case_data["check_sql_01"]:                    if case_data["case_id"] == 'case_0':                        db_actual_results = list({db_actual_results for db_actual_results in                                                  list(self.db.get_all(case_data["check_sql_01"]))})                        try:                            assert db_actual_results[0][0] == db_actual_results[0][1]                            assert db_actual_results[0][2] == case_data["json"]["sourceCode"]                            assert db_actual_results[0][3] == case_data["json"]["sourceTrxId"]                            assert db_actual_results[0][4] == case_data["json"]["sourceDocNumber"]                            assert db_actual_results[0][5] == case_data["json"]["companyCode"]                            assert db_actual_results[0][6] == case_data["json"]["country"]                            assert db_actual_results[0][7] == case_data["json"]["trxTypeCode"]                            assert db_actual_results[0][8] == case_data["json"]["vendorNum"]                            assert db_actual_results[0][9] == case_data["json"]["vendorName"]                            assert db_actual_results[0][10] == case_data["json"]["invoiceNum"]                            assert db_actual_results[0][11] == int(case_data["json"]["invoiceAmount"])                            assert db_actual_results[0][12] == int(case_data["json"]["invoiceLines"][0]["sourceLineId"])                            assert db_actual_results[0][13] == case_data["json"]["invoiceLines"][0]["trxSubtypeCode"]                            assert db_actual_results[0][14] == int(case_data["json"]["invoiceLines"][0]["lineAmount"])                            assert db_actual_results[0][15] == '0'                            assert db_actual_results[0][16] == None                            assert db_actual_results[0][17] == case_data["json"]["invoiceLines"][0]["channel"]                            assert db_actual_results[0][18] == case_data["json"]["invoiceLines"][0]["product"]                            assert db_actual_results[0][19] == int(case_data["json"]["invoiceLines"][0]["costCenter"])                            logging.info('断言成功,数据成功生成至应付发票临时表中，且发票行、发票头数据生成均正确')                        except KeyError as e:                            logging.info(f'断言失败,数据生成错误:{e}')                    elif  case_data["case_id"] == 'case_1':                        db_actual_results = list({db_actual_results for db_actual_results in                                                  self.db.get_all(case_data["check_sql_01"])})                        try:                            assert db_actual_results[0][0] == db_actual_results[0][1]                            assert db_actual_results[0][2] == case_data["json"][1]["sourceCode"]                            assert db_actual_results[0][3] ==  db_actual_results[0][4] == 'N'                            assert db_actual_results[0][5] == "1492-校验'invoiceLines[0].业务类型关联字段':业务类型编码'OSJ102'应该有明细"                            logging.info('断言成功,数据成功生成至应付发票临时表中，且状态为N,数据为无效数据')                        except KeyError as e:                            logging.info(f'断言失败,数据生成错误:{e}')                    elif  case_data["case_id"] == 'case_2':                        db_actual_results = list({db_actual_results for db_actual_results in                                                  self.db.get_all(case_data["check_sql_01"])})                        try:                            assert db_actual_results[0][0] == db_actual_results[0][1]                            assert db_actual_results[0][2] == case_data["json"][1]["sourceCode"]                            assert db_actual_results[0][3] ==  db_actual_results[0][4] == 'N'                            assert db_actual_results[0][5] == "1154-校验'invoiceAmount':must not be null"                            logging.info('断言成功,数据成功生成至应付发票临时表中，且状态为N,数据为无效数据')                        except KeyError as e:                            logging.info(f'断言失败,数据生成错误:{e}')            except AssertionError as i:                logging.error("用例{}生成数据{}--执行失败!".format(case_data["title"], case_data["case_id"]))                logging.debug(                    "用例{}生成数据{}--失败请求参数：{}".format(case_data["title"], case_data["case_id"], case_data["json"]))                logging.error("用例{}生成数据{}--失败请求返回参数：{}".format(case_data["title"], case_data["case_id"], result))                logging.error("用例{}生成数据{}--报错信息：{}".format(case_data["title"], case_data["case_id"], i))                logging.debug("用例{}生成数据{}--预期结果：{}".format(case_data["title"], case_data["case_id"], expected))                raise i            else:                logging.info("用例LGS115生成数据：{}-{}--执行通过".format(case_data["title"], case_data["case_id"]))if __name__ == '__main__':    self_test_LGS115 = TestReceivableLGS115()    self_test_LGS115.test_receivable_LGS115()