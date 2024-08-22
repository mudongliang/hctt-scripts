import re
import json
import argparse

def check_spacing(line, line_num):
    issues = {}

    # 检查中英文之间是否有空格
    zh_en_pattern = r'[\u4e00-\u9fff][a-zA-Z]|[a-zA-Z][\u4e00-\u9fff]'
    matches = re.finditer(zh_en_pattern, line)
    for match in matches:
        start, end = match.span()
        content = line[start:end]
        key = f"行 {line_num}，列 {start+1}"
        if "中英文之间需要空格" not in issues:
            issues["中英文之间需要空格"] = {}
        issues["中英文之间需要空格"][key] = content

    # 检查中文与数字之间的空格
    zh_num_pattern = r'[\u4e00-\u9fff][0-9]|[0-9][\u4e00-\u9fff]'
    matches = re.finditer(zh_num_pattern, line)
    for match in matches:
        start, end = match.span()
        content = line[start:end]
        key = f"行 {line_num}，列 {start+1}"
        if "中文与数字之间需要空格" not in issues:
            issues["中文与数字之间需要空格"] = {}
        issues["中文与数字之间需要空格"][key] = content

    return issues

def check_punctuation(line, line_num):
    issues = {}

    # 检查全角标点与其他字符之间不应有空格，排除全角标点后直接接换行符或句尾的情况
    punctuation_spacing_pattern = r'(\s+[\u3000-\u303F\uFF00-\uFFEF]|\s+[\u3000-\u303F\uFF00-\uFFEF]\s+(?=\S))'
    matches = re.finditer(punctuation_spacing_pattern, line)
    for match in matches:
        start, end = match.span()
        content = line[start:end].strip()
        key = f"行 {line_num}，列 {start+1}"
        if "全角标点与其他字符之间不应有空格" not in issues:
            issues["全角标点与其他字符之间不应有空格"] = {}
        issues["全角标点与其他字符之间不应有空格"][key] = content

    # 检查使用全角中文标点，支持"（"和"）"
    punctuation_correct_pattern = r'[a-zA-Z0-9]（|）[a-zA-Z0-9]'
    matches = re.finditer(punctuation_correct_pattern, line)
    for match in matches:
        start, end = match.span()
        content = line[start:end]
        # 允许中文括号前面是英文或数字的情况
        if content != '' and content[0].isalnum():
            continue
        key = f"行 {line_num}，列 {start+1}"
        if "使用全角中文标点，检查括号是否正确" not in issues:
            issues["使用全角中文标点，检查括号是否正确"] = {}
        issues["使用全角中文标点，检查括号是否正确"][key] = content

    # 检查英文整句使用半角标点，排除特殊情况
    full_width_in_english = re.finditer(
        r'(?<![，。；])([a-zA-Z]+[\s-]+[a-zA-Z\s-]+){3,}(?![（）])[\u3000-\u303F\uFF00-\uFFEF]', 
        line
    )
    for match in full_width_in_english:
        start, end = match.span()
        content = line[start:end]
        key = f"行 {line_num}，列 {start+1}"
        if "英文整句应使用半角标点" not in issues:
            issues["英文整句应使用半角标点"] = {}
        issues["英文整句应使用半角标点"][key] = content

    return issues

def check_document(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    all_issues = {}

    for i, line in enumerate(lines):
        line_num = i + 1
        spacing_issues = check_spacing(line, line_num)
        punctuation_issues = check_punctuation(line, line_num)

        # 合并所有问题
        for key, value in {**spacing_issues, **punctuation_issues}.items():
            if key not in all_issues:
                all_issues[key] = {}
            all_issues[key].update(value)

    return all_issues

def main():
    parser = argparse.ArgumentParser(description="检查Markdown文档中的中英文标点与空格问题")
    parser.add_argument("filename", type=str, help="需要检查的Markdown文档路径")
    args = parser.parse_args()

    issues = check_document(args.filename)
    if issues:
        print(json.dumps(issues, indent=4, ensure_ascii=False))
    else:
        print("文档符合规范，没有发现问题。")

if __name__ == "__main__":
    main()
