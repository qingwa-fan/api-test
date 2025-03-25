from py_page.main_page import MainPage


class TestGoods:

    # 测试在首页搜索商品的用例
    def test_search_goods_by_name(self, base_driver, goods="文具"):
        goods_name_list = MainPage(base_driver).search_goods_name(goods)
        for name in goods_name_list:
            assert goods in name

    # 测试进入商品详情页面
    def test_goto_goods_detail_page(self, base_driver, index=2):
        MainPage(base_driver).goto_goods_detail_page(index)