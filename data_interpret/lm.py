# @Author: weirdgiser
# @Date: 2025/1/10
# @Function:
from dotenv import load_dotenv
load_dotenv()
from enum import StrEnum
from langchain_community.llms.tongyi import Tongyi, BaseLLM


class ModelTypeEnum(StrEnum):
    QWEN_PLUS = "qwen-plus"
    QWEN_PLUS_1125 = "qwen-plus-1125"
    QWEN_PLUS_1127 = "qwen-plus-1127"
    QWEN_MAX = "qwen-max"


def debug_model_search(model: BaseLLM, question, iteration=1):
    for i in range(iteration):
        r = model.invoke(question)
        print(f"Answer {i}")
        print(r)

class ModelFactory:
    @classmethod
    def create_model(cls, model_type: str, enable_search: bool = True, max_retries=3):
        return Tongyi(model=model_type,
                      max_retries=max_retries,
                      model_kwargs=dict(enable_search=enable_search, temperature=0.1))


if __name__ == "__main__":
    model_enable_search = ModelFactory.create_model(model_type=ModelTypeEnum.QWEN_PLUS_1125, enable_search=True)
    model_no_search = ModelFactory.create_model(model_type=ModelTypeEnum.QWEN_PLUS_1125, enable_search=False)
    print(model_enable_search._default_params)
    print(model_no_search._default_params)
    question = """
        2025年最新技术动态，邓紫棋2024惠州演唱会
    """
    print("===No Search===")
    debug_model_search(model_no_search, question=question)
    print("===Search===")
    debug_model_search(model_enable_search, question=question)
