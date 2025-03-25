import os
import pytest
import allure
from common.contants import DATA_DIR
from common.read_json import ReadJson
from common.handle_request import HandleRequest
from common.handle_oracle import HandleDb
from common.config import conf
from common.my_log import Logger


TEST_DATA_PLAN = os.path.join(DATA_DIR, "test_fdp_payment_fns106_fns107.json")

logging = Logger(__name__).get_logger()
@allure.feature('应付付款接口_FNS106_FNS107')
@allure.testcase(conf.get("project_url", "url"), "测试地址：{}".format(conf.get("project_url", "url")))
class TestPaymentFNS107:
    # 准备
    json_object = ReadJson(TEST_DATA_PLAN)
    json_datas = json_object.read_json()
    cases = json_datas["cases"]
    http = HandleRequest()
    db = HandleDb()

    @classmethod
    def setup_class(self):
        logging.info('------>执行前置操作,删除已存在的测试数据')
        # 依次删除应付发票临时表、原始表头/行中FNS106数据
        self.db.del_data("DELETE  FROM FDP_AP_INVOICE_HEADER_ORIGIN_TEMP WHERE  SOURCE_TRX_ID ='FNS-20230625001'")
        self.db.del_data("DELETE  FROM FDP_AP_INVOICE_LINE_ORIGIN_TEMP  WHERE SOURCE_LINE_ID ='20230625001'")
        self.db.del_data("DELETE  FROM FDP_AP_INVOICE_HEADER_ORIGIN WHERE SOURCE_TRX_ID ='FNS-20230625001'")
        self.db.del_data("DELETE  FROM FDP_AP_INVOICE_LINE_ORIGIN WHERE SOURCE_LINE_ID ='20230625001'")
        # 依次删除应付付款临时表、原始表头/行中FNS107数据
        self.db.del_data("DELETE FROM FDP_AP_PAYMENT_HEADER_ORIGIN_TEMP WHERE SOURCE_TRX_ID ='FNS107_202306251001'")
        self.db.del_data("DELETE FROM FDP_AP_PAYMENT_LINE_ORIGIN_TEMP WHERE SOURCE_LINE_ID ='202306251001'")
        self.db.del_data("DELETE FROM FDP_AP_PAYMENT_HEADER_ORIGIN WHERE SOURCE_TRX_ID ='FNS107_202306251001'")
        self.db.del_data("DELETE FROM FDP_AP_PAYMENT_LINE_ORIGIN WHERE SOURCE_LINE_ID ='202306251001'")

    @classmethod
    def teardown_class(self):
        logging.info('------>执行后置操作,清理测试数据')
        # 依次删除应付发票临时表、原始表头/行中FNS106数据
        self.db.del_data("DELETE  FROM FDP_AP_INVOICE_HEADER_ORIGIN_TEMP WHERE  SOURCE_TRX_ID ='FNS-20230625001'")
        self.db.del_data("DELETE  FROM FDP_AP_INVOICE_LINE_ORIGIN_TEMP  WHERE SOURCE_LINE_ID ='20230625001'")
        self.db.del_data("DELETE  FROM FDP_AP_INVOICE_HEADER_ORIGIN WHERE SOURCE_TRX_ID ='FNS-2023062500'")
        self.db.del_data("DELETE  FROM FDP_AP_INVOICE_LINE_ORIGIN WHERE SOURCE_LINE_ID ='20230625001'")
        # 依次删除应付付款临时表、原始表头/行中FNS107数据
        self.db.del_data("DELETE FROM FDP_AP_PAYMENT_HEADER_ORIGIN_TEMP WHERE SOURCE_TRX_ID ='FNS107_202306251001'")
        self.db.del_data("DELETE FROM FDP_AP_PAYMENT_LINE_ORIGIN_TEMP WHERE SOURCE_LINE_ID ='202306251001'")
        self.db.del_data("DELETE FROM FDP_AP_PAYMENT_HEADER_ORIGIN WHERE SOURCE_TRX_ID ='FNS107_202306251001'")
        self.db.del_data("DELETE FROM FDP_AP_PAYMENT_LINE_ORIGIN WHERE SOURCE_LINE_ID ='202306251001'")
        self.db.close()

    @pytest.fixture()
    # request.param：用于获取测试的请求参数
    def case_data(self, request):
        casedata = request.param
        return casedata

    @allure.title("测试业务类型FNS107是否正确生成数据")
    @allure.story('业务类型FNS107测试用例')
    @pytest.mark.parametrize('case_data', cases, indirect=True)
    def test_payment_FNS107(self, case_data,base_headers):
        with allure.step("准备FNS107测试数据"):
            FNS106_url = conf.get("project_url", "url") + case_data["FNS106_url"]
            FNS107_url = conf.get("project_url", "url") + case_data["FNS107_url"]
            method = case_data["method"]
            # 预期结果
            FNS106_expected = case_data["FNS106_expected"]
            FNS107_expected = case_data["FNS107_expected"]
            print(FNS106_expected)
            print(FNS107_expected)
        # 调用应付发票接口，生成FNS106数据
        with allure.step("执行接口请求,生成FNS106数据"):
            response = self.http.send(url=FNS106_url, method=method, json=case_data["FNS106_json"],headers=base_headers)
            FNS106_result = response.json()
            # result = response.text
            print(FNS106_result)
        with allure.step("执行接口请求,生成FNS107数据"):
            response = self.http.send(url=FNS107_url, method=method, json=case_data["FNS107_json"],headers=base_headers)
            FNS107_result = response.json()
            print(FNS107_result)
        with allure.step("进行预期结果断言"):
            try:
                # 请求体断言
                assert FNS106_expected["code"] == FNS106_result["code"]
                assert FNS106_expected["msg"] in FNS106_result["msg"]
                assert FNS107_expected["code"] == FNS107_result["code"]
                assert FNS107_expected["msg"] == FNS107_result["msg"]
                logging.info('断言成功,返回信息正确')

                # 数据库断言--判断应付发票原始表中,FNS106数据是否准确
                if case_data["check_sql_01"]:
                    if case_data["case_id"] == 'case_0':
                        db_actual_results = list({db_actual_results for db_actual_results in
                                                  list(self.db.get_all(case_data["check_sql_01"]))})
                        # print(db_actual_results)
                        try:
                            assert db_actual_results[0][0] == case_data["FNS106_json"]["sourceTrxId"]
                            logging.info('断言成功,数据成功生成至应付发票原始表中')
                        except KeyError:
                            logging.info('断言失败,数据生成错误')

                # 数据库断言--判断应付付款原始表中,FNS107数据是否准确
                if case_data["check_sql_02"]:
                    if case_data["case_id"] == 'case_0':
                        db_actual_results_02 = list({db_actual_results_02 for db_actual_results_02 in
                                                  list(self.db.get_all(case_data["check_sql_02"]))})
                        print(db_actual_results_02)
                        try:
                            assert db_actual_results_02[0][0] == case_data["FNS107_json"]["apPaymentHeaderReqs"][0]["sourceTrxId"]
                            logging.info('断言成功,数据生成至应付付款原始表中')
                        except KeyError:
                            logging.info('断言失败，测试不通过')


            except AssertionError as i:
                logging.error("用例{}生成数据{}--执行失败!".format(case_data["title"], case_data["case_id"]))
                logging.debug(
                    "用例{}生成数据{}--失败请求参数：{}".format(case_data["title"], case_data["case_id"], case_data["FNS107_json"]))
                logging.error("用例{}生成数据{}--失败请求返回参数：{}".format(case_data["title"], case_data["case_id"], FNS107_result))
                logging.error("用例{}生成数据{}--报错信息：{}".format(case_data["title"], case_data["case_id"], i))
                logging.debug("用例{}生成数据{}--预期结果：{}".format(case_data["title"], case_data["case_id"], FNS107_expected))
                raise i
            else:
                logging.info("用例FNS107生成数据：{}-{}--执行通过".format(case_data["title"], case_data["case_id"]))


if __name__ == '__main__':
    self_payment_FNS107 = TestPaymentFNS107()
    self_payment_FNS107.test_payment_FNS107()