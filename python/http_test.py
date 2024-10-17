# coding=utf-8
import requests
import json


domain_port = 'http://localhost:5001'
add_user_url = domain_port+'/admin-create-users'
modify_user_roles_url = domain_port+'/admin-modify-user-roles'
query_user_url = domain_port+'/admin-query-userlist'

'''
logined_username = result["logined_username"]
        new_user_email = result["new_user_email"]
        firstname = result["firstname"]
        lastname = result["lastname"]
        password = result["password"]

'''
def test_add_user():


    url = add_user_url
    data = {
        "logined_username": "admin",
        "new_user_email": "user1@gmail.com",
        "firstname": "firstname1",
        "lastname": "lastname1",
        "password": "123456"
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print('code:', response.status_code)
    print(response.text)




def test_modify_user_roles():
    url = modify_user_roles_url
    data = {
        "logined_username": "admin",
        "user_email": "user1@gmail.com",
        "to_roles": "2"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print('code:', response.status_code)
    print(response.text)




def test_query_user():
    url = query_user_url
    data = {
        "logined_username": "admin"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, data=json.dumps(data), headers=headers)
    print('code:', response.status_code)
    print('body:')
    print(response.text)



if __name__ == '__main__':
    print("http_test start")
    #test_query_user()
    #test_add_user()
    #test_modify_user_roles()


