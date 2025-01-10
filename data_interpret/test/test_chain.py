"""
模型：启用搜索/不启用搜索
数据：提供GDP增速数据/不提供
"""
import unittest
import pandas as pd
from data_interpret.core.chains import DefaultGDPGrowthRateChain
from data_interpret.lm import ModelFactory, ModelTypeEnum
from data_interpret.utils import generate_quarter_periods
from ddt import data, ddt
llm_enable_search = ModelFactory.create_model(ModelTypeEnum.QWEN_PLUS_1125, enable_search=True)
llm_no_search = ModelFactory.create_model(ModelTypeEnum.QWEN_PLUS_1125, enable_search=False)

df = pd.read_excel("../samples/中国GDP增长率.xlsx")

gdp_periods = generate_quarter_periods(range(2020, 2023))

@ddt
class TestGDPChainWithLLMSearch(unittest.TestCase):
    def setUp(self):
        self.chain = DefaultGDPGrowthRateChain(llm=llm_enable_search)

    @data(*gdp_periods)
    def test_interpret(self, period):
        print("当前周期：", period)
        result = self.chain.interpret(current_period=period, reference_data=df.values)
        print(result)
        self.assertIsNotNone(result)
@ddt
class TestGDPChainWithLLMNoSearch(unittest.TestCase):
    def setUp(self):
        self.chain = DefaultGDPGrowthRateChain(llm=llm_no_search)

    @data(*gdp_periods)
    def test_interpret(self, period):
        print("当前周期：", period)
        result = self.chain.interpret(current_period=period, reference_data=df.values)
        print(result)
        self.assertIsNotNone(result)


if __name__ == '__main__':
    import os
    from BeautifulReport import BeautifulReport
    suite = unittest.TestSuite()
    print("modules", os.getcwd())
    from data_interpret.test import test_chain
    tests = unittest.TestLoader().loadTestsFromModule(test_chain)
    suite.addTests(tests)
    report = BeautifulReport(suite)
    report.report(description="中国GDP增速-提供历年数据", report_dir=".",
                  filename=f"2020-2024中国GDP增速-qwen-plus-1125-2.html", theme='theme_cyan')
