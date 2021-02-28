import json
import os

FILE_NAME = 'setting.json'

def load():

    if os.path.isfile(FILE_NAME) == False:
        # 設定ファイルが存在しない
        # デフォルト値を書き込み
        template = {
            'MAIL':'hoge'
            ,'PASS':'******'        
        }
        with open(FILE_NAME, "w") as f:
            json.dump(template,f)

    with open(FILE_NAME,'r') as f:
        tmp = json.load(f)
        return tmp


