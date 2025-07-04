from ai import gemini
from data import const
import re

CONTEXT = """
            안녕하세요. 성수동 설비업체입니다. 
            
            %본문%
            
            끝맺음말입니다. 
        """

def get_body():
    gemini.init_gemini()
    response = gemini.create_content([const.CONTENT_EX1, const.CONTENT_EX2])
    print(response)
    response = response.replace("**", "")
    delimiter_pattern = r'  |\n+'
    contents = [item.strip() for item in re.split(delimiter_pattern, response)]
    print(contents)
    index = 0
    for content in contents:
        print(f"[{index}]: {content}")
        index += 1

def get_header_footer():
    global CONTEXT
    header_footer =  [item.strip() for item in re.split("%본문%", CONTEXT)]
    return header_footer

head_foot = get_header_footer()
header, footer = head_foot[0], head_foot[1]
print(f"[header] = {header}")
get_body()
print(f"[footer] = {footer}")

def link_lists():
    list1 = [1, 2, 3]
    list2 = [2, 3, 4]
    list3 = [3, 4, 5]
    lists = []
    lists.extend(list1)
    lists.extend(list2)
    lists.extend(list3)
    print(lists)

link_lists()