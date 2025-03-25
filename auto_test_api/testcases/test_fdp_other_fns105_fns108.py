import osimport pytestimport allurefrom common.contants import DATA_DIRfrom common.read_json import ReadJsonfrom common.handle_request import HandleRequestfrom common.handle_oracle import HandleDbfrom common.config import conffrom common.my_log import LoggerTEST_DATA_PLAN = os.path.join(DATA_DIR, "test_fdp_other_fns105_fns108.json")logging = Logger(__name__).get_logger()@allure.feature('其他业务接口2_FNS105_FNS108')@allure.testcase(conf.get("project_url", "url"), "测试地址：{}".format(conf.get("project_url", "url")))class TestOtherFNS108:    # 准备    json_object = ReadJson(TEST_DATA_PLAN)    json_datas = json_object.read_json()    cases = json_datas["cases"]    http = HandleRequest()    db = HandleDb()    @classmethod    def setup_class(self):        logging.info('------>执行前置操作,删除已存在的测试数据')        # 依次删除付款接口临时表、原始表头中FNS105数据        self.db.del_data("DELETE FROM FDP_AP_PAYMENT_HEADER_ORIGIN_TEMP WHERE SOURCE_TRX_ID ='FNS105_20230625001'")        self.db.del_data("DELETE FROM FDP_AP_PAYMENT_HEADER_ORIGIN WHERE SOURCE_TRX_ID ='FNS105_20230625001'")        # 依次删除其他业务接口临时表、汇总表头中FNS108数据        self.db.del_data("DELETE FROM FDP_FIN_COMMON_HEADER_TEMP WHERE SOURCE_TRX_ID ='FNS-2023062566001'")        self.db.del_data("DELETE FROM FDP_FIN_COMMON_HEADER_T WHERE SOURCE_TRX_ID ='FNS-2023062566001'")    @classmethod    def teardown_class(self):        logging.info('------>执行后置操作,清理测试数据')        # 依次删除付款接口临时表、原始表头中FNS105数据        self.db.del_data("DELETE FROM FDP_AP_PAYMENT_HEADER_ORIGIN_TEMP WHERE SOURCE_TRX_ID ='FNS105_20230625001'")        self.db.del_data("DELETE FROM FDP_AP_PAYMENT_HEADER_ORIGIN WHERE SOURCE_TRX_ID ='FNS105_20230625001'")        # 依次删除其他业务接口临时表、汇总表头中FNS108数据        self.db.del_data("DELETE FROM FDP_FIN_COMMON_HEADER_TEMP WHERE SOURCE_TRX_ID ='FNS-2023062566001'")        self.db.del_data("DELETE FROM FDP_FIN_COMMON_HEADER_T WHERE SOURCE_TRX_ID ='FNS-2023062566001'")        self.db.close()    @pytest.fixture()    # request.param：用于获取测试的请求参数    def case_data(self, request):        casedata = request.param        return casedata    @allure.title("测试业务类型FNS108是否正确生成数据")    @allure.story('业务类型FNS108测试用例')    @pytest.mark.parametrize('case_data', cases, indirect=True)    def test_other_FNS108(self, case_data,base_headers):        with allure.step("准备FNS108测试数据"):            FNS105_url = conf.get("project_url", "url") + case_data["FNS105_url"]            FNS108_url = conf.get("project_url", "url") + case_data["FNS108_url"]            method = case_data["method"]            # 预期结果            FNS105_expected = case_data["FNS105_expected"]            FNS108_expected = case_data["FNS108_expected"]        # 调用其他业务接口2，生成FNS108数据        with allure.step("执行接口请求,生成FNS105数据"):            response = self.http.send(url=FNS105_url, method=method, json=case_data["FNS105_json"],headers=base_headers)            FNS105_result = response.json()        with allure.step("执行接口请求,生成FNS108数据"):            response = self.http.send(url=FNS108_url, method=method, json=case_data["FNS108_json"],headers=base_headers)            FNS108_result = response.json()        with allure.step("进行预期结果断言"):            try:                # 请求体断言                assert FNS105_expected["code"] == FNS105_result["code"]                assert FNS105_expected["msg"] in FNS105_result["msg"]                assert FNS108_expected["code"] == FNS108_result["code"]                assert FNS108_expected["msg"] == FNS108_result["msg"]                logging.info('断言成功,返回信息正确')                # 数据库断言--判断应付付款临时表中,FNS105数据是否准确                if case_data["check_sql_01"]:                    if case_data["case_id"] == 'case_0':                        db_actual_results_01 = list({db_actual_results_01 for db_actual_results_01 in                                                  list(self.db.get_all(case_data["check_sql_01"]))})                        print(db_actual_results_01)                        print(db_actual_results_01[0][0])                        print(case_data["FNS105_json"]["apPaymentHeaderReqs"][0]["sourceTrxId"])                        try:                            assert db_actual_results_01[0][0] == case_data["FNS105_json"]["apPaymentHeaderReqs"][0]["sourceTrxId"]                            logging.info('断言成功,数据生成至应付付款临时表中')                        except KeyError:                            logging.info('断言失败，测试不通过')                # 数据库断言--判断应付付款原始表中,FNS105数据是否准确                if case_data["check_sql_02"]:                    if case_data["case_id"] == 'case_0':                        db_actual_results_02 = list({db_actual_results_02 for db_actual_results_02 in                                                  list(self.db.get_all(case_data["check_sql_02"]))})                        print(db_actual_results_02)                        try:                            assert db_actual_results_02[0][0] == case_data["FNS105_json"]["apPaymentHeaderReqs"][0]["sourceTrxId"]                            logging.info('断言成功,数据生成至应付付款原始表中')                        except KeyError:                            logging.info('断言失败，测试不通过')                # 数据库断言--断言数据FNS108是否生成至其他业务接口临时表中，并且断言数据的准确性                if case_data["check_sql_03"]:                    origin_actul_results_03 = list({origin_actul_results_03 for origin_actul_results_03 in                                               list(self.db.get_all(case_data["check_sql_03"]))})                    print(origin_actul_results_03)                try:                    assert origin_actul_results_03[0][0] == case_data["FNS108_json"]["sourceTrxId"]                    logging.info('数据FNS108成功生成至其他业务接口汇总头表中')                except KeyError as e:                    logging.info(f'数据FNS108未生成至其他业务接口汇总头表中：{e}')                # 数据库断言--断言数据FNS108是否生成至其他业务接口汇总行表中，并且断言数据的准确性                if case_data["check_sql_04"]:                    origin_actul_results_04 = list({origin_actul_results_04 for origin_actul_results_04 in                                               list(self.db.get_all(case_data["check_sql_04"]))})                try:                    assert origin_actul_results_04[0][0] == case_data["FNS108_json"]["sourceTrxId"]                    logging.info('数据FNS108成功生成至其他业务接口汇总表中')                except KeyError as e:                    logging.info(f'数据FNS108未生成至其他业务接口汇总表中：{e}')            except AssertionError as i:                logging.error("用例{}生成数据{}--执行失败!".format(case_data["title"], case_data["case_id"]))                logging.debug(                    "用例{}生成数据{}--失败请求参数：{}".format(case_data["title"], case_data["case_id"], case_data["FNS108_json"]))                logging.error("用例{}生成数据{}--失败请求返回参数：{}".format(case_data["title"], case_data["case_id"], FNS108_result))                logging.error("用例{}生成数据{}--报错信息：{}".format(case_data["title"], case_data["case_id"], i))                logging.debug("用例{}生成数据{}--预期结果：{}".format(case_data["title"], case_data["case_id"], FNS108_expected))                raise i            else:                logging.info("用例FNS108生成数据：{}-{}--执行通过".format(case_data["title"], case_data["case_id"]))if __name__ == '__main__':    self_other_FNS108 = TestOtherFNS108()    self_other_FNS108.test_other_FNS108()