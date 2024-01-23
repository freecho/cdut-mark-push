# 定义一个函数来比较两个数组并找出新获取的成绩中的新增部分
def compare_mark(previous, new):
    # 将之前的成绩转化为集合，以便快速比较
    previous_set = set(tuple(item) for item in previous)

    # 检查新成绩中的每个项是否在之前的成绩中
    new_items = [item for item in new if tuple(item) not in previous_set]

    # 返回新增的成绩项
    return new_items