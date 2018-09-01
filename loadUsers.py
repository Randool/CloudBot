""":return user list"""

users_bak = [
    ["品味之家", "宁波", False, 'G'], 
    ["两对", "宁波", False, 'G'],
    ["Pepper*79", "成都", True, 'W'],
#    ["{ Aeonni }", "杭州", True, 'M'],
    ["尼玛来啦~", "长沙", True, 'W'],
    ["A.", "长沙", True, "W"],
    ["想吃柠檬", "长沙", True, "W"],
#    ["EWING", "长沙", True, 'M'], 
#    ["棖", "长沙", True, 'W'], 
#    ["乔越", "长沙", True, 'W'],
#    ["陶印荣", "长沙", True, 'M'],
#    ["稷下歌吟", "长沙", True, 'W'],
]


def get_users(file='user_info.txt'):
    """
    :return: [name / position / individual / sex]
    """
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_list = []
    for line in lines:
        if len(line) <= 1 or line[0] == '#':
            continue
        user = line.strip('\ufeff\n').split(',')
        user[2] = True if user[2] == 'True' else False
        new_list.append(user)

    return new_list


def test_func():
    new_list = get_users()
    for i in range(len(new_list)):
        if new_list[i][0] != users_bak[i][0]:
            print(new_list[i], "error")
        else:
            print("Right")

