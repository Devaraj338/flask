import requests
users = input("which task you wanted to perform? ")

if users== "get":
    res = requests.get("http://127.0.0.1:5000/users")
    print(res.text)

elif users== "getone":
    user_id = input("enter which user you want")
    res = requests.get(f"http://127.0.0.1:5000/users/{user_id}")
    print(res.text)

elif users=="post":
    new_users_data = {
        'name' : input("enter a name "),
        'emailid' : input("enter a email "),
        'city'   :input("enter the city name ")
    }
    res = requests.post("http://127.0.0.1:5000/users", json=new_users_data)
    print(res.json())

elif users=="put":
    user_id_to_update = input("enter the id no")
    update_data = {
        'name' : input("enter a name"),
        'emailid' : input("enter a emailid"),
        'city': input("enter a city name")
    }
    response = requests.put(f'http://127.0.0.1:5000/users/{user_id_to_update}', json=update_data)
    print(response.json())

elif users=="delete":
    user_id_to_delete = input("enter the number")
    response = requests.delete(f'http://127.0.0.1:5000/users/{user_id_to_delete}')
    print(response.json())

else:
    print("Enter valid user to perform this action")

