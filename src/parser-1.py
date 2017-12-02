import argparse
import csv
import json

def main():
	examples = []
	with open('/Users/mattchan/Projects/yhack_2017/data/fake_or_real_news.csv', 'r', newline='', encoding='utf-8') as f:
		csv_parser = csv.reader(f)
		count = 0

		for row in csv_parser:
			# if count == 1:
			# 	print(row)
			obj = {"example": row[0], "target": {"title": row[1], "body":row[2]}, "label": row[3]}
			examples.append(obj)
			count += 1

	with open('/Users/mattchan/Projects/yhack_2017/data/fake_or_real_news.json', mode='w+', encoding='utf-8') as f2:
		json.dump(examples, f2, ensure_ascii=False)

if __name__ == '__main__':
	# parser = argparse.ArgumentParser()
	# parser.add_argument("filename")
	# args = parser.parse_arguments()
	main()