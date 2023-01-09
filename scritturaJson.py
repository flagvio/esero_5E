import json

# a Python object (dict):
n = {
  "name": "John",
  "age": 30,
  "city": "New York"
}

# some JSON:
x =  '{ "name":"John", "age":30, "city":"New York"}'

# parse x:
y = json.loads(x)

# the result is a Python dictionary: print(y["age"])
# convert into JSON: z = json.dumps(n)
# the result is a JSON string: print(z)



f = open("demofile.json","a")
f.write(x)
print("Scrittura su file")
f.close()