import osimport pytestimport allurefrom common.contants import DATA_DIRfrom common.read_json import ReadJsonfrom common.handle_request import HandleRequestfrom common.handle_oracle import HandleDbfrom common.config import conffrom common.my_log import LoggerTEST_DATA_PLAN = os.path.join(DATA_DIR, "test_fdp_receive_osj107.json")logging = Logger(__name__).get_logger()@allure.feature('应收事务处理接口_OSJ107')@allure.testcase(conf.get("project_url", "url"), "测试地址：{}".format(conf.get("project_url", "url")))class TestReceivableOSJ107():    # 准备    json_object = ReadJson(TEST_DATA_PLAN)    json_datas = json_object.read_json()    cases = json_datas["cases"]    http = HandleRequest()    db = HandleDb()    @classmethod    def setup_class(self):        logging.info('------>执行前置操作,删除已存在的测试数据')        # 删除应收事务临时表中数据        self.db.del_data("DELETE  FROM XX_AR_TRX_DETAIL_TEMP  WHERE TRX_TYPE = 'OSJ107'  "                         "AND SOURCE_TRX_ID ='OSJ107_20230604002'")        # 删除应收事务明细表中数据        self.db.del_data("DELETE   FROM XX_AR_TRX_DETAIL  WHERE TRX_TYPE = 'OSJ107'  "                         "AND SOURCE_TRX_ID ='OSJ107_20230604002'")        # 删除推送任务表中数据        self.db.del_data("DELETE  FROM FDP_AUTO_PUSH_TASK_HEADER_T  WHERE TRX_TYPE_CODE = 'OSJ107' "                         "AND COMPANY_CODE ='1601' AND STATUS = 0")    @classmethod    def teardown_class(self):        logging.info('------>执行后置操作,清理测试数据')        # 删除应收事务临时表中数据        self.db.del_data("DELETE  FROM XX_AR_TRX_DETAIL_TEMP  WHERE TRX_TYPE = 'OSJ107'  "                         "AND SOURCE_TRX_ID ='OSJ107_20230604002'")        # 删除应收事务明细表中数据        self.db.del_data("DELETE   FROM XX_AR_TRX_DETAIL  WHERE TRX_TYPE = 'OSJ107'  "                         "AND SOURCE_TRX_ID ='OSJ107_20230604002'")        # 删除推送任务表中数据        self.db.del_data("DELETE  FROM FDP_AUTO_PUSH_TASK_HEADER_T  WHERE TRX_TYPE_CODE = 'OSJ107' "                         "AND COMPANY_CODE ='1601' AND STATUS = 0")        self.db.close()    @pytest.fixture()    # request.param：用于获取测试的请求参数    def case_data(self, request):        casedata = request.param        return casedata    @allure.title("测试业务类型OSJ107是否正确生成数据，并且可以成功汇总且推送")    @allure.story('业务类型OSJ107测试用例')    @pytest.mark.parametrize('case_data', cases, indirect=True)    def test_receivable_OSJ107(self, case_data,base_headers):        with allure.step("准备OSJ107测试数据"):            url = conf.get("project_url", "url") + case_data["url"]            method = case_data["method"]            # 预期结果            expected = case_data["expected"]        # 调用应收事务接口，生成OSJ107数据        with allure.step("执行接口请求,生成OSJ107数据"):            response = self.http.send(url=url, method=method, json=case_data["json"],headers=base_headers)            result = response.json()            # result = response.text        with allure.step("进行预期结果断言"):            try:                # 请求体断言                assert expected["code"] == result["code"]                assert expected["msg"] == result["msg"]                # 数据库断言--断言数据是否生成至应收事务临时表中，判断SOURCE_TRX_ID                if case_data["check_sql_temp"]:                    temporary_results_id = list({SOURCE_TRX_ID for SOURCE_TRX_ID in self.db.get_all(case_data["check_sql_temp"])})                    try:                        assert temporary_results_id[0][0] == case_data["json"][0]["sourceTrxId"]                        logging.info('断言成功,数据成功生成至应收事务临时表中')                    except KeyError as e:                        logging.info(f'断言失败,数据未生成至应收事务临时表中:{e}')                # 数据库断言--断言数据是否生成至应收事务正式表中，判断SOURCE_TRX_ID                if case_data["check_sql_formal"]:                    formal_results = list({SOURCE_TRX_ID for SOURCE_TRX_ID in self.db.get_all(case_data["check_sql_formal"])})                    try:                        assert formal_results[0][0] == case_data["json"][0]["sourceTrxId"]                        logging.info('断言成功,数据成功生成至应收事务正式表中')                    except KeyError as e :                        logging.info(f'断言失败,数据未生成至应收事务正式表中:{e}')                # 数据库断言--此时，数据未进行汇总，也未进行推送，断言SUMMARY_STATUS、RCT_STATUS是否为0                if case_data["check_sql_formal_status"]:                    formal_status = list({status for status in                                        self.db.get_all(case_data["check_sql_formal_status"])})                    try:                        assert formal_status[0][0] == 0                        assert formal_status[0][1] == 0                        logging.info('断言成功,SUMMARY_STATUS、RCT_STATUS此时都为0')                    except KeyError as e:                        logging.info(f'断言失败,SUMMARY_STATUS、RCT_STATUS不正确:{e}')            except AssertionError as i:                logging.error("用例{}生成数据{}--执行失败!".format(case_data["title"], case_data["case_id"]))                logging.debug(                    "用例{}生成数据{}--失败请求参数：{}".format(case_data["title"], case_data["case_id"], case_data["json"]))                logging.error("用例{}生成数据{}--失败请求返回参数：{}".format(case_data["title"], case_data["case_id"], result))                logging.error("用例{}生成数据{}--报错信息：{}".format(case_data["title"], case_data["case_id"], i))                logging.debug("用例{}生成数据{}--预期结果：{}".format(case_data["title"], case_data["case_id"], expected))                raise i            else:                logging.info("用例OSJ107生成数据：{}-{}--执行通过".format(case_data["title"], case_data["case_id"]))        # 汇总OSJ107，并且新增推送        with allure.step("测试数据准备-新增推送-OSJ107"):            taskurl = conf.get("project_url", "url") + case_data["taskUrl"]            taskmethod = case_data["method"]            # 预期结果            expected = case_data["expected"]            # 调用新增推送接口，新增B2B166推送任务        with allure.step("调用新增推送接口，新增OSJ107推送任务"):            response = self.http.send(url=taskurl, method=taskmethod, json=case_data["task_json"], headers=base_headers)            result = response.json()        with allure.step("进行预期结果断言"):            try:                # 请求体断言                assert expected["code"] == result["code"]                assert expected["msg"] == result["msg"]                # 数据库断言--断言数据是否成功新增推送，推送状态是否等于0                if case_data["check_sql_push_status"]:                    push_status = list({STATUS for STATUS in                                         list(self.db.get_all(case_data["check_sql_push_status"]))})                    try:                        assert push_status[0][0] == '0'                        logging.info('断言成功,成功新增推送，且推送状态此时为0')                    except KeyError as e:                        logging.info(f'断言失败,新增推送失败:{e}')            except AssertionError as i:                logging.error("用例{}新增推送{}--执行失败!".format(case_data["title"], case_data["case_id"]))                logging.debug(                    "用例{}新增推送{}--失败请求参数：{}".format(case_data["title"], case_data["case_id"], case_data["json"]))                logging.error("用例{}新增推送{}--失败请求返回参数：{}".format(case_data["title"], case_data["case_id"], result))                logging.error("用例{}新增推送{}--报错信息：{}".format(case_data["title"], case_data["case_id"], i))                logging.debug("用例{}新增推送{}--预期结果：{}".format(case_data["title"], case_data["case_id"], expected))                raise i            else:                logging.info("用例新增推送：{}-{}--执行通过".format(case_data["title"], case_data["case_id"]))if __name__ == '__main__':    self_test_OSJ107 = TestReceivableOSJ107()    self_test_OSJ107.test_receivable_OSJ107()