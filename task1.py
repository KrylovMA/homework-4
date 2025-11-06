import json
"""
вывести первые 2 строки из файла purchase_log.txt в формате:
user_id: 'category'
"""
result = {}
with open('purchase_log.txt', 'r', encoding='utf-8') as f:
    next(f)  # Пропускаем заголовок
    for i in range(2):  # Берем 2 строки
        line = next(f)
    # for line in f:  # Обрабатываем все строки
        data = json.loads(line.strip())
        result[data['user_id']] = data['category']

for user_id, category in result.items():
    print(f"{user_id}: '{category}'")

