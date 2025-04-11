import json

def process_striver_sheet(filename):
    with open(filename, 'r',encoding='utf-8') as file:
        data = json.load(file)

    problems = {}
    for step in data['sheetData']:
        for topic in step['topics']:
            title = topic['title']
            lc_link = topic['lc_link']
            if title and lc_link:
                problems[title] = lc_link

    return problems

def save_problems(problems, output_filename='striver_problems.py'):
    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write("problems = {\n")
        for title, link in problems.items():
            if link.startswith("https://leetcode.com"):
                file.write(f"    \"{title}\": \"{link}\",\n")
        file.write("}\n")

# Usage
filename = 'striver-sde-sheet.json'
problems = process_striver_sheet(filename)
save_problems(problems)

print(f"Processed {len(problems)} problems.")
print("Data saved to 'striver_problems.py'")
