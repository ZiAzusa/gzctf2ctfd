import requests
import hashlib
import time
import os
try:
    import ujson as json
except ImportError:
    import json
from template import *

host = "127.0.0.1:12345" # 在这里填写GZCTF的主机

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,en-GB;q=0.6,ja;q=0.5",
    "Cookie": "", # 在这里填写GZCTF的管理员Cookie
    "Referer": f"http://{host}/admin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
}

def get_api(api, params={}, host=host, headers=headers):
    for i in range(3):
        try:
            req = requests.get(f"http://{host}{api}", params=params, headers=headers)
            if req.status_code == 200:
                return req
        except requests.exceptions.ConnectionError:
            if i >= 2:
                raise ConnectionError

def class2dic(obj):
    dic = {}
    for attr in [attr for attr in dir(obj) if not attr.startswith("_")]:
        dic[attr] = getattr(obj, attr)
    return dic

with open("export/db/challenges.json", "r") as f:
    challenges_db = json.load(f)
    challenge_id = challenges_db['results'][-1]['id'] if challenges_db['results'] else 0
with open("export/db/dynamic_challenge.json", "r") as f:
    dynamic_challenge_db = json.load(f)
with open("export/db/dynamic_docker_challenge.json", "r") as f:
    dynamic_docker_challenge_db = json.load(f)
with open("export/db/files.json", "r") as f:
    files_db = json.load(f)
    file_id = files_db['results'][-1]['id'] if files_db['results'] else 0
with open("export/db/flags.json", "r") as f:
    flags_db = json.load(f)
    flag_id = flags_db['results'][-1]['id'] if flags_db['results'] else 0
with open("export/db/hints.json", "r") as f:
    hints_db = json.load(f)
    hint_id = hints_db['results'][-1]['id'] if hints_db['results'] else 0

game_json = get_api(f"/api/edit/games", {"count": 30}).text
game_data = json.loads(game_json)
for game in game_data['data'][::-1]:
    print("adding game: "+game['title'])
    challenge_json = get_api(f"/api/edit/games/{game['id']}/challenges").text
    challenge_data = json.loads(challenge_json)
    for challenge in challenge_data:
        challenge_id += 1
        info_json = get_api(f"/api/edit/games/{game['id']}/challenges/{challenge['id']}").text
        info = json.loads(info_json)
        print("adding challenge: " + info['title'])
        class Challenge(Challenge):
            id = challenge_id
            name = info['title']
            description = info['content']
            value = info['originalScore']
            category = game['title']+"."+info['tag']
            type = "dynamic_docker" if "Container" in info['type'] else "dynamic"
        challenges_db['count']  += 1
        challenges_db['results'].append(class2dic(Challenge()))
        class DynamicChallenge(DynamicChallenge):
            id = challenge_id
            initial = info['originalScore']
            minimum = info['originalScore'] * info['minScoreRate']
            decay = info['difficulty'] * 6
        dynamic_challenge_db['count'] += 1
        dynamic_challenge_db['results'].append(class2dic(DynamicChallenge()))
        if "Container" in info['type']:
            class DynamicDockerChallenge(DynamicDockerChallenge):
                id = challenge_id
                memory_limit = info['memoryLimit']
                cpu_limit = info['cpuCount']
                dynamic_score = 1 if info['minScoreRate'] != 1 else 0
                docker_image = info['containerImage']
                redirect_type = "http" if info['tag'] == "Web" else "direct"
                redirect_port = info['containerExposePort']
            dynamic_docker_challenge_db['count'] += 1
            dynamic_docker_challenge_db['results'].append(class2dic(DynamicDockerChallenge()))
        if info['attachment']:
            file_id += 1
            print("downloading: "+info['attachment']['url'])
            file = requests.get("http://"+host+info['attachment']['url']).content
            file_md5 = hashlib.md5(file).hexdigest()
            if not os.path.exists("export/uploads/"+file_md5):
                os.mkdir("export/uploads/"+file_md5)
            else:
                file_md5 += str(int(time.time()))
                os.mkdir("export/uploads/"+file_md5)
            with open("export/uploads/"+file_md5+"/"+info['attachment']['url'].split("/")[-1], "wb+") as f:
                f.write(file)
            print("downloaded: "+file_md5+"/"+info['attachment']['url'].split("/")[-1])
            class File(File):
                id = file_id
                location = file_md5+"/"+info['attachment']['url'].split("/")[-1]
                challenge_id = challenge_id
            files_db['count'] += 1
            files_db['results'].append(class2dic(File()))
        if info['flags'] and not "Dynamic" in info['type']:
            for flag_data in info['flags']:
                flag_id += 1
                class Flag(Flag):
                    id = flag_id
                    challenge_id = challenge_id
                    content = flag_data['flag']
                flags_db['count'] += 1
                flags_db['results'].append(class2dic(Flag()))
        if info['hints']:
            for hint in info['hints']:
                hint_id += 1
                class Hint(Hint):
                    id = hint_id
                    challenge_id = challenge_id
                    content = hint
                hints_db['count'] += 1
                hints_db['results'].append(class2dic(Hint()))
        time.sleep(0.5)

with open("export/db/challenges.json", "w+") as f:
    f.write(json.dumps(challenges_db))
with open("export/db/dynamic_challenge.json", "w+") as f:
    f.write(json.dumps(dynamic_challenge_db))
with open("export/db/dynamic_docker_challenge.json", "w+") as f:
    f.write(json.dumps(dynamic_docker_challenge_db))
with open("export/db/files.json", "w+") as f:
    f.write(json.dumps(files_db))
with open("export/db/flags.json", "w+") as f:
    f.write(json.dumps(flags_db))
with open("export/db/hints.json", "w+") as f:
    f.write(json.dumps(hints_db))
print("done")
