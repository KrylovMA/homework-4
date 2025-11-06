import csv
import json


def user_category_dictionary(purchase_log_path: str): # функция для построения словаря user_id -> category
	user_to_category = {}

	with open(purchase_log_path, "r", encoding="utf-8") as purchase_file:

		for line in purchase_file: # построчная 

			line = line.strip() 

			if not line: # обработка пустых
				continue

			try:
				to_dct = json.loads(line) # json в словарь

			except json.JSONDecodeError: 
				continue

			user_id = to_dct.get("user_id") # id из записи

			category = to_dct.get("category") # категория из записи

			if user_id and category and user_id != "user_id": # проверка что оба поля нашлись и не попал заголовок

				user_to_category[user_id] = category

	return user_to_category


def build_funnel(visit_log_path: str, purchase_log_path: str, funnel_output_path: str): # функция с 3 файлами

	user_to_category = user_category_dictionary(purchase_log_path) # передает файл в первую функцию

	with open(visit_log_path, "r", encoding="utf-8") as visit_file, open( # открывает visit log для чтения и funnel для записи
		funnel_output_path, "w", encoding="utf-8", newline=""

	) as funnel_file:

		reader = csv.DictReader(visit_file) # чтение visit log построчно

		fieldnames = ["user_id", "source", "category"] # столбцы для funnel

		writer = csv.DictWriter(funnel_file, fieldnames=fieldnames) # чтение записей как словарей по заголовку
		writer.writeheader()

		for row in reader: # цикл для обхода строк записей файла

			user_id = row.get("user_id") # берется id из текущей строки
            # обработка ошибок
			if not user_id: 
				continue

			category = user_to_category.get(user_id) # поиск категории по id 

			if category is None:
				continue

			writer.writerow({   # запись id source и категории 

				"user_id": user_id,
				"source": row.get("source"),
				"category": category,
			})


if __name__ == "__main__":
	build_funnel(
		visit_log_path="visit_log.csv",
		purchase_log_path="purchase_log.txt",
		funnel_output_path="funnel.csv",
	)


