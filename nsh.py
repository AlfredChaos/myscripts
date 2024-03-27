from cnocr import CnOcr
from flask import Flask, request, jsonify


def parse_pictures():
    ocr = CnOcr()
    res = ocr.ocr('nsh01.png')
    index = 0
    for k in res:
        name = res[index]['text']
        kill = res[index+2]['text']
        assist = res[index+3]['text']
        resource = res[index+4]['text']
        index = index+5
        print(f"name={name}, kill={kill}, assist={assist}, resource={resource}")
        print("*"*30)
        if index >= len(res):
            break


app = Flask(__name__)

data = {
    "boss": "xx",
    "blade": "yy",
    "images": ['1', '2'],
    "excludes": "12,32"
}


@app.route('/submit', methods=['POST'])
def submit():
    pass


@app.route('/reset', methods=['POST'])
def reset():
    pass


@app.route('/battle_token', methods=['GET'])
def get_battle_token():
    pass


@app.route('/month_card', methods=['GET'])
def get_month_card():
    pass


@app.route('/milky_tea', methods=['GET'])
def get_milky_tea():
    pass

# 定义一个路由，用于GET请求


@app.route('/api/greeting', methods=['GET'])
def get_greeting():
    name = request.args.get('name', 'Guest')  # 获取查询参数，如果没有则默认为'Guest'
    return jsonify({'message': f'Hello, {name}!'})

# 定义一个路由，用于POST请求


@app.route('/api/message', methods=['POST'])
def post_message():
    data = request.get_json()  # 获取JSON格式的请求数据
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    message = data.get('message', '')
    return jsonify({'received_message': message})


# 启动Flask应用程序
if __name__ == '__main__':
    app.run(debug=True)
