# @Author: weirdgiser
# @Date: 2025/1/10
# @Function:
import os
from pathlib import Path
from ..lm import BaseLLM
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema, PydanticOutputParser
from data_interpret.interface import Chain, InterpretResult
from pydantic.fields import Field
TEMPLATE_DIR = Path(__file__).parent / "templates"


class GDPInterpretResultModel(InterpretResult):
    result: str  = Field(description="中国GDP增速解读结果")
    reason: str  = Field(description="给出该解读的理由")
    current_period: str  = Field(description="当前周期")
    current_value: str = Field(description="当前周期的GDP增速指标")

class DefaultGDPGrowthRateChain(Chain):
    PROMPT_FILE = os.path.join(TEMPLATE_DIR, "gdp.ptext")
    def __init__(self, llm: BaseLLM, max_length="200"):
        self.llm = llm
        self.output_parser = self._init_output_parser()
        format_instructions = self.output_parser.get_format_instructions()
        system_prompt = PromptTemplate.from_file(DefaultGDPGrowthRateChain.PROMPT_FILE)
        partial_prompt = system_prompt.partial(max_length=max_length, format_instructions=format_instructions)
        self.chain = partial_prompt | self.llm | self.output_parser

    def interpret(self, current_period, reference_data, reference_info=None, *args, **kwargs):
        result = self.chain.invoke(input=dict(reference_data=reference_data, current_period=current_period))
        return result



    def _init_output_parser(self):
        # response_schemes = [
        #     ResponseSchema(name="result", description="中国GDP增速解读结果", type='string'),
        #     ResponseSchema(name="reason", description="给出该解读的理由", type='string'),
        #     ResponseSchema(name="current_period", description="当前周期", type='string'),
        #     ResponseSchema(name="current_value", description="当前周期的GDP增速指标", type='string')
        # ]
        # output_parser = StructuredOutputParser(response_schemas=response_schemes)
        # return output_parser
        return PydanticOutputParser(pydantic_object=GDPInterpretResultModel)

