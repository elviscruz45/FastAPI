import json


user={"nombre":"Elvis","Apellidos":"Cruz","email":"elviscruz45@gmail.com"}
user1={"nombre":"Jose","Apellidos":"Sarmiento","email":"jose@gmail.com"}
user2={"nombre":"Carlos","Apellidos":"Chullo","email":"carlos@gmail.com"}

with open("file.json","r+",encoding="utf-8") as f:
    #print(type(f))
    results=json.loads(f.read())
    #print(type(results))
    results.append(user)
    #print(type(results))
    f.seek(0)

    f.write(json.dumps(results))
    print(type(results))
