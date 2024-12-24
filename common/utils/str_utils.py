import uuid
import re
import os


def remove_emojis(input_string) -> str:
    # 使用正则表达式删除所有表情符号
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # 表情符号
                               u"\U0001F300-\U0001F5FF"  # 符号与杂项符号
                               u"\U0001F680-\U0001F6FF"  # 交通和地图符号
                               u"\U0001F700-\U0001F77F"  # 国际音标扩展符号
                               u"\U0001F780-\U0001F7FF"  # 表情符号补充
                               u"\U0001F800-\U0001F8FF"  # 语言补充
                               u"\U0001F900-\U0001F9FF"  # 符号与象形文字补充
                               u"\U0001FA00-\U0001FA6F"  # 扑克牌
                               u"\U0001FA70-\U0001FAFF"  # 旗帜（Emoji表情）
                               u"\U0001F004"  # 单个符号-标签
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', input_string)


def remove_spaces_and_tabs(input_string) -> str:
    text = input_string.replace(" ", "").replace("\t", "")
    return text

def remove_special_characters(input_string) -> str:
    # 定义正则表达式模式，匹配特殊符号，同时保留 .．！？~、,
    pattern = r'[^\w\s.．！？~、,，。]'  # 这个模式匹配除了字母、数字、空格和指定符号之外的所有字符

    # 使用 re.sub() 函数删除匹配的特殊字符
    cleaned_string = re.sub(pattern, '', input_string)

    return cleaned_string

def get_uuid(msg_id):
    if not msg_id:
        msg_id = f"{uuid.uuid4()}"
    return msg_id



def is_all_special_chars(string):
    ''' 判断字符是否全部是这些特殊标点字符'''
    pattern = r'^[。,，？?！!。．;\u2000-\u206F\u2E00-\u2E7F\\\'\"#$%&()*+\-/:<=>?@\[\]^_`{|}~\s\n ]+$'
    match_result = re.compile(pattern).match(string)
    return match_result is not None


def test():
    text = ''' 。

在参观完滇王金印后，您还可以继续探索云南省博物馆中其他珍贵文物和历史展品，进一步了解云南地区'''
    text1 = ''' 。

游'''
    content = text1.replace('\n', '')
    for word in text1:
        print(word)
    temp = ''
    for word in text:
        temp += word
        match_result = re.match(r"^(.{10,}).*?[？?！!。．\n;；]", temp)

        end = None if not match_result else match_result.end()
        print(f'{temp} -  \n end: {end}， end-str: {temp[:end]}  结果： {match_result != None}')

    return
    # 测试用例
    input_str = '滇王金印是在1956年在昆明市晋宁区石寨山被发现的'
    output_str = replace_digits_with_chinese(input_str)
    print(output_str)  # 输出: 一九五六年

    # 示例用法
    string1 = "!!!???..."
    print(is_all_special_chars(string1))  # 输出: True

    string2 = "Hello, World!"
    print(is_all_special_chars(string2))  # 输出: False

    string3 = "你好!"
    print(is_all_special_chars(string3))  # 输出: False

    string4 = "你好@！……!"
    print(is_all_special_chars(string4))  # 输出: False

    string5 = "\n\n。,，？?！!。．"
    print(is_all_special_chars(string5))  # 输出: False


def to_camel_case_hyphen(text):
    text = text.replace("-request", '')
    words = text.split('-')
    return ''.join(word.capitalize() for word in words)

def get_work_dir()->str:
    return os.getcwd()