import json
import re
import base64
import os

def extract_profile(data):
    return data['graphql']['user']


def extract_following(data):   
    friendship_api_url=r'https://www.instagram.com/api/v1/.*/following/'
    contents= [entry['response']['content']for entry in data['log']['entries'] 
        if re.match(friendship_api_url,entry['request']['url'])
    ]

    #extract json data
    users=[]
    for content in contents:
        if 'text' not in content:
            continue
        text=content['text']

        if 'encoding' in content and content['encoding']=='base64':
            decoded_text = base64.b64decode(text)
            decoded_string = str(decoded_text, 'utf-8')
            user_json=json.loads(decoded_string)
            users.extend(user_json['users'])
        else:
            user_json=json.loads(text)
            users.extend(user_json['users'])
    return users

    #save json data
def extract_persons(person):
    with open(f'./data/{person}/{person}.har','r',errors='ignore') as f:
        data = json.loads(f.read())
        followings=extract_following(data)

    with open(f'./data/{person}/{person} details.json','r') as f:
        data = json.loads(f.read())
        profile=extract_profile(data)
        
    output= {
        'general':profile,
        'followings':followings
    }

    return output, profile['id']

def extract_all():

    persons=os.listdir('./data')
    users={}
    for person in persons:
        output, id=extract_persons(person)
        users[id]=output

    with open(f'./out/people.json','w') as f:
        f.write(json.dumps(users))
        

extract_all()