# @Author: weirdgiser
# @Date: 2025/1/10
# @Function:
def generate_quarter_periods(years):
    quarter_indicators = ["第一季度", "第二季度", "第三季度", "第四季度"]
    data = []
    for y in years:
        for q in quarter_indicators:
            data.append(f"{y}{q}")
    return data

if __name__ == "__main__":
    r = generate_quarter_periods(range(2016, 2025))
    print(r)