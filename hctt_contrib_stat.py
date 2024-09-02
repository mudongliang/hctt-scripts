import os
import re
from collections import defaultdict

#使用方式：
#1、clone TranslateProject仓库到本地
#2、将本程序放在本地仓库中，运行

# 获取脚本所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))
# 构建 sources 文件夹的路径
project_path = os.path.join(script_dir, "sources")

# 用于存储贡献数据的字典
contribution_data = defaultdict(lambda: {"collect": 0, "translate": 0, "proofread": 0, "publish": 0})

# 正则表达式用于匹配元数据
metadata_pattern = re.compile(r"(\w+):\s*(\S+)")

# 遍历 sources 文件夹
for root, dirs, files in os.walk(project_path):
    for file in files:
        if file.endswith(".md"):
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                metadata = dict(metadata_pattern.findall(content))

                # 根据元数据更新贡献数据
                if "collector" in metadata:
                    contribution_data[metadata["collector"]]["collect"] += 1
                if "translator" in metadata:
                    contribution_data[metadata["translator"]]["translate"] += 1
                if "proofreader" in metadata:
                    contribution_data[metadata["proofreader"]]["proofread"] += 1
                if "publisher" in metadata:
                    contribution_data[metadata["publisher"]]["publish"] += 1

# 输出贡献数据视图
header = "{:<15} {:<8} {:<10} {:<10} {:<8}".format("GitHub ID", "Collect", "Translate", "Proofread", "Publish")
print(header)
print("-" * len(header))

for github_id, contributions in contribution_data.items():
    row = "{:<15} {:<8} {:<10} {:<10} {:<8}".format(
        github_id,
        contributions['collect'],
        contributions['translate'],
        contributions['proofread'],
        contributions['publish']
    )
    print(row)
