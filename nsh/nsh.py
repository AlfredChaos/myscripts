import os
import random
from cnocr import CnOcr
from flask import Flask, request, jsonify

# 考虑一个问题，生成一个令牌token，标记这是某一次帮战的数据，设定缓存保存的期限，超时删除
# 一次提交一个token
# 重置时清除本次token及token下的数据
# 每次请求api，带着本次帮战的token，获取对应的缓存数据，获取不到则报错
# 记录全局数据的数据结构应该被改善，token作为key，每个token代表一次帮战，value是字典
# 字典中包含：群龙十人，四项标准前三，全场帮战数据
# submit新增token，若token已存在则默认覆盖
# reset删除token
# 抽奖接口带着token过来，从缓存中获取战绩并进行抽奖
# data = {
#     'name': {
#         'kill': '12',
#         'assist': '12',
#         'heal': '12万',
#         'take': '12万',
#         'blood': '12万',
#         'damage': '12万',
#     }
# }
all_data = {}
PIC_TYPE_STRATEGY = 'strategy'
PIC_TYPE_TREAT = 'treat'
PIC_TYPE_OUTPUT = 'output'
PIC_TYPES = [PIC_TYPE_STRATEGY,
             PIC_TYPE_TREAT,
             PIC_TYPE_OUTPUT]
TITLE_LEADER = 'leader'
TITLE_BLADE = 'blade'
TITLES = [TITLE_LEADER,
          TITLE_BLADE]


def parse_pictures(pic_type):
    global all_data
    directory = f"./{pic_type}/"
    for root, dirs, entries in os.walk(directory):
        for entry in entries:
            path = f"./{pic_type}/{entry}"
            ocr = CnOcr()
            res = ocr.ocr(path)
            index = 0
            for k in res:
                name = res[index]['text']
                num_1 = res[index+2]['text']
                num_2 = res[index+3]['text']
                index = index+5
                if pic_type == PIC_TYPE_STRATEGY:
                    all_data[name]['kill'] = num_1
                    all_data[name]['assist'] = num_2
                elif pic_type == PIC_TYPE_TREAT:
                    all_data[name]['heal'] = num_1
                    all_data[name]['take'] = num_2
                elif pic_type == PIC_TYPE_OUTPUT:
                    all_data[name]['blood'] = num_1
                    all_data[name]['damage'] = num_2
                else:
                    raise Exception("picture type unsupport")
                if index >= len(res):
                    break


def lottery(participants, num_winners=1):
    # 确保获奖者数量不超过参与者数量
    if num_winners > len(participants):
        raise ValueError(
            "Number of winners cannot be greater than the number of participants.")

    winners = random.sample(participants, num_winners)
    return winners


def sort_data_by_key_word(key_word):
    entries = []
    global all_data
    for key, name_data in all_data.items():
        # 检查key_word是否在name_data中
        if key_word not in name_data:
            raise KeyError(f"The key_word '{key_word}' is not in the data.")

        entries.append(name_data)

    # 对条目列表根据key_word_value进行排序
    sorted_entries = sorted(entries, key=lambda x: x[key_word], reverse=True)
    return sorted_entries


def save_picture(pic_type):
    if pic_type not in PIC_TYPES:
        raise Exception(f'unsupport picture types')
    if pic_type in request.files[pic_type]:
        images = request.files['pic_type']
        for image in images:
            img_data = image.read()
            with open(f'./{pic_type}/{image.filename}', 'wb') as f:
                f.write(img_data)


app = Flask(__name__)


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    leader = data.get('leader', '')
    blade = data.get('blade', '')
    excludes = data.get('excludes', '')
    losts = excludes.split(',')

    save_picture(PIC_TYPE_STRATEGY)
    save_picture(PIC_TYPE_TREAT)
    save_picture(PIC_TYPE_OUTPUT)
    global all_data
    all_data = {}
    parse_pictures(PIC_TYPE_STRATEGY)
    parse_pictures(PIC_TYPE_TREAT)
    parse_pictures(PIC_TYPE_OUTPUT)

    result = {
        "leader": leader,
        "blade": blade
    }
    entries = sort_data_by_key_word(key_word='blood')
    result["killings"] = [entries[0], entries[1], entries[2]]
    entries = sort_data_by_key_word(key_word='damage')
    result["buildings"] = [entries[0], entries[1], entries[2]]
    entries = sort_data_by_key_word(key_word='heal')
    result["healings"] = [entries[0], entries[1], entries[2]]
    entries = sort_data_by_key_word(key_word='take')
    result["takings"] = [entries[0], entries[1], entries[2]]

    return jsonify(result)


@app.route('/reset', methods=['POST'])
def reset():
    global all_data
    all_data = {}
    return jsonify({'message': f"reset successfully"})


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
