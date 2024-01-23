import json
import time

import requests

from login import Login
from bs4 import BeautifulSoup
import tools

# 两次更新的时间间隔 单位：秒
rest_time = 600


def run(username, token):
    # 获取已经登入的session对象
    login = Login(username=username)
    session = login.getSession()

    # 开课时间【2023-2024-1】
    html_content = session.get(login.config["url"]["cjcx"] + "?kksj=2023-2024-1").text

    soup = BeautifulSoup(html_content, 'html.parser')
    # 获取成绩表格
    table = soup.find('table', {'id': 'dataList'})
    # 初始化一个列表来存储结果
    course_mark = []
    # 遍历表格中的所有行
    for row in table.find_all('tr')[1:]:  # [1:] 跳过表头
        # 找到所有的单元格
        cells = row.find_all('td')

        # 获取课程名称和成绩
        # 课程名称在第四个单元格，成绩在第五个
        course_name = cells[3].get_text(strip=True)
        grade = cells[4].get_text(strip=True)

        # 将课程名称和成绩添加到列表中
        course_mark.append((course_name, grade))

    # 存储成绩
    try:
        # 读取文件
        with open("mark.json", "r") as file:
            # 尝试加载JSON内容
            local_mark = json.load(file)

        # 之前已经获取过成绩
        if len(local_mark.get(username, [])) > 0:
            # 获取新增的成绩
            new_mark = tools.compare_mark(local_mark[username], course_mark)
            # 成绩有所更新
            if len(new_mark) > 0:
                # 推送更新
                post_content = ""
                # 设置推送文本
                for course, score in new_mark:
                    post_content += f"课程名称：{course}，分数：{score}<br>"

                post_data = {
                    "token": token,
                    "title": "成绩更新",
                    "content": post_content
                }

                response = requests.post(data=post_data, url=login.config["url"]["send"])
                if response.status_code == 200:
                    print("推送更新成功")
                else:
                    print("推送更新失败,返回状态码：", response.status_code)
        # 首次获取成绩
        else:
            # 设置推送文本
            post_content = "首次获取成绩成功，获取到以下成绩：<br>"
            for course, score in course_mark:
                post_content += f"课程名称：{course}，分数：{score}<br>"
            post_content += "后续将每隔一段时间自动更新成绩并推送！"

            post_data = {
                "token": token,
                "title": "成功",
                "content": post_content
            }

            response = requests.post(data=post_data, url=login.config["url"]["send"])
            if response.status_code == 200:
                print("首次推送成功")
            else:
                print("首次推送失败,返回状态码：", response.status_code)

        # 更新成绩
        local_mark[username] = course_mark
        # 数据更新后，重新写入文件
        with open("mark.json", "w") as file:
            json.dump(local_mark, file)

    except FileNotFoundError:
        # 如果文件不存在，创建文件
        with open("mark.json", "w") as file:
            json.dump({username: {}}, file)
            exit("mark.json文件不存在，现在已创建，请重新运行")

    except Exception as e:
        print(f"错误：{e}")



if __name__ == '__main__':

    while True:
        # 读取用户列表
        with open("user.json", "r") as f:
            users = json.load(f)
        for username, info in users.items():
            token = info["token"]
            run(username=username, token=token)

        time.sleep(rest_time)
