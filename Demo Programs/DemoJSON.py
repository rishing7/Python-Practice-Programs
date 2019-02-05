import json

demo = '''{"employee":[{"name":"John", "age":30, "city":"New York" }, {"name":"atul", "age":60, "city":"New York" }]}'''


data = json.loads(demo)
print(type(data))
print(type(data['employee']))
print(data['employee'][1]['name'])