def sort_data_by_key_word(data, key_word):
    result = {}
    entries = []
    for key, name_data in data.items():
        # 检查key_word是否在name_data中
        if key_word not in name_data:
            raise KeyError(f"The key_word '{key_word}' is not in the data.")

        entries.append(name_data)
        
    # 对条目列表根据key_word_value进行排序
    sorted_entries = sorted(entries, key=lambda x: x[key_word], reverse=True)
    for k in sorted_entries:
        result[k['name']] = k
    return result

# 示例数据
data = {
    'alfred': {
        'name': 'alfred',
        'kill': '12',
        'assist': '14',
        'heal': '12万',
        'take': '48万',
        'blood': '3万',
        'damage': '12万',
    },
    'chaos': {
        'name': 'chaos',
        'kill': '12',
        'assist': '14',
        'heal': '12万',
        'take': '48万',
        'blood': '1万',
        'damage': '12万',
    },
    'Ray': {
        'name': 'Ray',
        'kill': '12',
        'assist': '14',
        'heal': '12万',
        'take': '48万',
        'blood': '2万',
        'damage': '12万',
    }
}

# 调用函数并打印结果
sorted_list = sort_data_by_key_word(data, 'blood')
print(sorted_list)