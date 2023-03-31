import pytest
from core.xueqiu_app import XueQiuApp
from hamcrest import assert_that, close_to


class TestXueQiu:

    def setup_class(self):
        # 启动app
        self.xueqiuapp = XueQiuApp()

    def setup(self):
        self.main = self.xueqiuapp.start().goto_main()

    def teardown_class(self):
        self.xueqiuapp.stop()

    @pytest.mark.parametrize('search_key, search_result, price', [["alibaba", "BABA", 100]])
    def test_search1(self, search_key, search_result, price):
        # TODO 改脚本有一个BUG,即未应对弹出来的登录页面,后续增加特殊场景处理临时处理的功能
        """
        打开【雪球】应用首页
        点击搜索框，进入搜索页面
        向搜索输入框中输入【alibaba】
        点击搜索结果中的【阿里巴巴】
        切换到 tab 的【股票】
        找到 股票【阿里巴巴】的股票价格 price
        判断 price 在 110 上下 10%浮动
        :return:
        """
        # search_key = "alibaba"
        # search_result='BABA'
        print("search_result", search_result)
        stock_price = self.main.click_search(). \
            input_searchcontent(search_key). \
            click_searchresult(search_result). \
            goto_stock_tab().get_price()

        print("stock_price", stock_price)
        print("price", price)
        # hamcrest 接近某个值的范围
        assert_that(stock_price, close_to(price, price * 0.1))