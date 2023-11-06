import json

## Сохранение списка в файл в формате json
def save_groups(groups, filepath):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        json.dump(groups, outfile, ensure_ascii=False)