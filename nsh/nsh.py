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
# all_data = {
#     'token-123': {
#         'leader': 'alfred',
#         'blade': 'chaos',
#         'killings': ['alfred', 'chaos', 'ray'],
#         'buildings': ['alfred', 'jack', 'tom'],
#         'healings': ['jay', 'tom', 'tim'],
#         'takings': ['tim', 'tom', 'hum'],
#         'battle_token_winner': '',
#         'data': [{
#             'name': 'alfred',
#             '123': '123'
#         }]
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

# 一个字典，统计数据
# data = {
#     'alfred': {
#         'name': 'alfred',
#         'kills': '12',
#         '...'
#     }
# }
def parse_pictures(data, pic_type):
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
                data[name]['name'] = name
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


def sort_data_by_key_word(data, key_word):
    entries = []
    for key, name_data in data.items():
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
    token = data.get('token')
    if not token:
        return jsonify({'error': "token is required"}), 400
    leader = data.get('leader', '')
    blade = data.get('blade', '')
    # excludes = data.get('excludes', '')
    # losts = excludes.split(',')

    save_picture(PIC_TYPE_STRATEGY)
    save_picture(PIC_TYPE_TREAT)
    save_picture(PIC_TYPE_OUTPUT)
    global all_data
    data = {}
    parse_pictures(data, PIC_TYPE_STRATEGY)
    parse_pictures(data, PIC_TYPE_TREAT)
    parse_pictures(data, PIC_TYPE_OUTPUT)

    all_data[token][TITLE_LEADER] = leader
    all_data[token][TITLE_BLADE] = blade
    entries = sort_data_by_key_word(data, key_word='blood')
    all_data[token]["killings"] = [entries[0], entries[1], entries[2]]
    entries = sort_data_by_key_word(data, key_word='damage')
    all_data[token]["buildings"] = [entries[0], entries[1], entries[2]]
    entries = sort_data_by_key_word(data, key_word='heal')
    all_data[token]["healings"] = [entries[0], entries[1], entries[2]]
    entries = sort_data_by_key_word(data, key_word='take')
    all_data[token]["takings"] = [entries[0], entries[1], entries[2]]
    all_data[token]['data'] = entries

    return jsonify(all_data[token])


@app.route('/reset', methods=['POST'])
def reset():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    token = data.get('token')
    if not token:
        return jsonify({'error': "token is required"}), 400

    global all_data
    del all_data[token]
    return jsonify({'message': f"reset successfully"})


@app.route('/battle_token', methods=['POST'])
def get_battle_token():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    token = data.get('token')
    if not token:
        return jsonify({'error': "token is required"}), 400
    if token not in all_data:
        return jsonify({'error': 'upload data, please'}), 400
    
    participants = []
    leader = all_data[token][TITLE_LEADER]
    if leader:
        participants.append(leader)
    blade = all_data[token][TITLE_BLADE]
    if blade and blade not in participants:
        participants.append(blade)
    for name in all_data[token]['killings']:
        if name not in participants:
            participants.append(name)
    for name in all_data[token]['buildings']:
        if name not in participants:
            participants.append(name)
    for name in all_data[token]['healings']:
        if name not in participants:
            participants.append(name)
    for name in all_data[token]['takings']:
        if name not in participants:
            participants.append(name)
    
    global all_data
    winner = lottery(participants)
    all_data[token]['battle_token_winner'] = winner
    return jsonify({'winner': winner})


@app.route('/month_card', methods=['POST'])
def get_month_card():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    token = data.get('token')
    if not token:
        return jsonify({'error': "token is required"}), 400
    if token not in all_data:
        return jsonify({'error': 'upload data, please'}), 400
    
    participants = []
    battle_token_winner = all_data[token]['battle_token_winner']
    data = all_data[token]['data']
    for d in data:
        if d['name'] == battle_token_winner:
            continue
        participants.append(d['name'])
    
    winner = lottery(participants)
    return jsonify({'winner': winner})


@app.route('/milky_tea', methods=['POST'])
def get_milky_tea():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    token = data.get('token')
    if not token:
        return jsonify({'error': "token is required"}), 400
    if token not in all_data:
        return jsonify({'error': 'upload data, please'}), 400
    
    participants = []
    for d in all_data[token]['data']:
        participants.append(d['name'])
    winners = lottery(participants, num_winners=2)
    return jsonify({'winners': winners})


# 启动Flask应用程序
if __name__ == '__main__':
    app.run(debug=True)
