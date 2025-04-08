import numpy as np
import pandas as pd
from config_2 import WENJUAN, CHARACTERS, CHARACTER_NUM
import random
from datetime import datetime
def generate_samples():
    # 初始化结果列表
    result = []
    print(type(CHARACTERS))
    
    # 遍历每个角色
    for character_name, character_config in CHARACTERS.items():
        num_samples = character_config["num"]
        # 获取固定概率配置
        fixed_probabilities = character_config.get("fixed_probabilities", {})
        # 获取固定选项配置
        fixed_options = character_config.get("fixed_options", {})
        
        # 生成该角色的人数
        for _ in range(num_samples):
            sample = []
            # 遍历每个问题
            for question in WENJUAN:
                if question in fixed_options:
                    # 从固定选项中随机选择一个
                    option = random.choice(fixed_options[question])
                # 优先检查固定概率配置
                elif question in fixed_probabilities:
                    # 根据固定概率生成选项
                    probabilities = fixed_probabilities[question]
                    options = list(probabilities.keys())
                    probs = list(probabilities.values())
                    option = random.choices(options, weights=probs, k=1)[0]

                else:
                    # 使用正态分布生成选项
                    mean, var = character_config[question]
                    prob = np.random.normal(loc=mean, scale=var)#np.sqrt(var)
                    # 将概率值限制在0到1之间
                    prob = max(0, min(1, prob))
                    num_options = WENJUAN[question]
                    # 将概率映射到选项数字，确保在1到num_options之间
                    option = int(prob * num_options) + 1
                sample.append(str(option))
            result.append(sample)
    
    # 生成列名
    columns = [f"{i}" for i in  WENJUAN.keys()]
    # 创建DataFrame
    df = pd.DataFrame(result, columns=columns)
    # 输出到Excel
    current_time = datetime.now().strftime("%Y%m%d_%H%M")
    file_name = f"data/{current_time}.xlsx"
    df.to_excel(file_name, index=False)

if __name__ == "__main__":
    for i in WENJUAN.keys():
        WENJUAN[i] = WENJUAN[i] - 1
        # print(WENJUAN[i])
    generate_samples()
