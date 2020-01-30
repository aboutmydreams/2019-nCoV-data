from flask import Flask, make_response, request, g, jsonify
import json
import schedule
import medrxiv.get_medrxiv_data as med
import schedule


# 定时任务爬虫
def tasklist():
    with open("./key.json", 'r') as f:
        keyword = json.loads(f.read())

    def do_medrxiv_data():
        print("run!")
        med.get_list(keyword)
    # 清空任务
    schedule.clear()
    # 创建一个按秒间隔执行任务
    schedule.every(1).seconds.do(do_medrxiv_data)
    schedule.run_pending()


# 网络编程

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def get_paper():
    with open("./result.json", 'r') as f:
        temp = json.loads(f.read())
    return jsonify(data=temp)


if __name__ == '__main__':
    tasklist()
    app.run(debug=True)
