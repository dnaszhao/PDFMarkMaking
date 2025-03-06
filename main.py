import re

# 定义一个全局变量 offset，这里初始化为 0，不过在当前代码中未使用该变量
print('\n输入页码偏移量offset: ')
offset = input()


# 定义一个名为 process_pdf_bookmark 的函数，该函数接受两个参数：
# input_file 表示输入的目录文件的文件名，output_file 表示处理后输出的目录文件的文件名
def process_pdf_bookmark(input_file, output_file):
    # 以只读模式打开输入文件，并使用 UTF-8 编码
    with open(input_file, 'r', encoding='utf-8') as f:
        # 读取文件的所有行，并将每行内容作为一个元素存储在列表 lines 中
        lines = f.readlines()

    # 初始化一个空列表 output，用于存储处理后的目录行
    output = []
    # 遍历输入文件的每一行
    for line in lines:
        # 去除当前行前后的空白字符
        line = line.strip()
        # 如果当前行为空行，则跳过该行，继续处理下一行
        if not line:
            continue

        # 使用正则表达式搜索当前行末尾的连续数字，该数字代表页码
        page_match = re.search(r'(\d+)$', line)
        # 如果没有找到页码，则跳过该行，继续处理下一行
        if not page_match:
            continue

        # 提取匹配到的页码
        page = page_match.group(1)
        # 提取当前行中页码之前的内容，并去除前后的特殊字符，该内容为目录标题
        content_match = re.search(r'^[\u4e00-\u9fa5a-zA-Z\s()0-9=、]*', line)
        content = content_match.group()
        # 使用正则表达式匹配目录标题开头的数字编号，如 1、1.1、1.1.1 等
        level_match = re.match(r'^(\d+(?:\.\d+)*)\D*', content)
        if level_match:
            # 计算数字编号中 '.' 的数量，该数量代表目录的层级
            level = level_match.group(1).count('.')
            # 提取目录标题中数字编号之后的内容，并去除前后的空白字符
            title = content[level_match.end():].strip()
        else:
            # 如果没有匹配到数字编号，则认为该目录为顶级目录，层级为 0
            level = 0
            # 整个目录标题即为处理后的标题
            title = content

        # 根据目录的层级生成相应数量的制表符作为缩进
        indent = '\t' * level
        # 生成处理后的目录行，格式为：缩进 + 标题 + 页码
        output_line = f"{indent}{title}\t{str(int(page) + int(offset))}"
        # 将处理后的目录行添加到 output 列表中
        output.append(output_line)

    # 以写入模式打开输出文件，并使用 UTF-8 编码
    with open(output_file, 'w', encoding='utf-8') as f:
        # 将 output 列表中的所有目录行用换行符连接成一个字符串，并写入输出文件
        f.write('\n'.join(output))


# 使用示例，调用 process_pdf_bookmark 函数，处理输入目录文件，并将结果保存到输出目录文件中
process_pdf_bookmark('输入目录文件.txt', '输出目录文件.txt')
