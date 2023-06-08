import json

class LoadJson:
    json_file = open('utils\\test_data.json',"r", encoding='UTF-8')
    json_data = json.load(json_file).get('data')

    json_env_data = json_data.get('env')
    json_user_data = json_data.get('user')
    json_predefined_data = json_data.get('predefined_values')
    json_query_data = json_data.get('query')    

    # print(json_predefined_data.get('bookmark_permlist'))