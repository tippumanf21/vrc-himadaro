import settings
import vrcpy
import datetime
import time
import os
from tqdm import tqdm# 進捗
from rich.console import Console
from rich.table import Table

# 出力値クリア
os.system('cls')

# 初期化
setting = settings.load()
client = vrcpy.Client()
print('ログイン中...')
client.login(setting['ID'],setting['PASS'])

# ユーザ情報
users = {}

while(True):
    time.sleep(1)

    now = datetime.datetime.now()

    disp_list = []
    users_checked = []

    try:
        print('フレンド情報取得中...')
        for friend in tqdm(client.fetch_full_friends()):
            disp = {}
            time.sleep(1)
            
            #### debug #####
            #print(friend._dict)
            ################
            
            ##############################
            worldId = friend._dict['worldId']
            
            if(friend._dict['worldId'] == 'private' or friend._dict['worldId'] == 'offline'):
                # 取得できない場合はcontinue（ワールド/インスタンス情報で判定するため）
                continue
            
            instanceId = friend._dict['instanceId']
            #print(instanceId)
            ##############################
            # 滞在場所取得
            try:
                world_res = client.api.call("/worlds/"+worldId)
                world = vrcpy.objects.World(client,world_res['data'])
                instance = world.fetch_instance(instanceId)
                location = "{}/{}".format(worldId,instanceId)
            except:
                # 何らかの例外が発生した場合は無視して続行する
                continue

            # 表示名称
            id = friend._dict['id']
            users_checked.append(id)
            if id not in users:
                # usersディクショナリに初めてのユーザ
                users[id] = {}
                users[id]['displayName'] = ''
                users[id]['worldName'] = ''
                users[id]['location'] = ''
                users[id]['instanceCapacity'] = ''
                users[id]['instanceStayStart'] = None
                users[id]['instanceStayTime'] = None

            # 基本情報セット
            users[id]['displayName'] = friend._dict['displayName']
            users[id]['worldName'] = world._dict['name']
            users[id]['instanceCapacity'] = str(instance._dict['n_users']) + '/' + str(instance._dict['capacity'])
            
            if(users[id]['location'] != location):
                # ロケーションが変更された
                users[id]['location'] = location # ロケーション更新
                users[id]['instanceStayStart'] = now # 滞在開始時間更新
            # ロケーション滞在時間計算
            users[id]['instanceStayTime'] = str(now - users[id]['instanceStayStart'])
            users[id]['instanceStayTimeSec'] = int((now - users[id]['instanceStayStart']).seconds)
        
        # ログイン→ログオフ状態になったユーザを除外する
        for key in list(users):
            cnt = len([user_id for user_id in users_checked if user_id == key])
            if cnt == 0:
                users.pop(key)

        # 表示内容ソート
        users_list = []
        for key in users:
            users_list.append(users[key])
        #print(users_list)
        users_sorted = sorted(users_list,key=lambda x:x['instanceStayTimeSec'])
        #print(users_sorted)
        # コンソールクリア
        os.system('cls')
        console = Console()
        table = Table(show_header=True,header_style="bold magenta")
        table.add_column('フレンド')
        table.add_column('ワールド')
        table.add_column('滞在時間')
        for user in users_sorted:
            table.add_row(user['displayName'][:10]
                ,user['worldName'][:20] + "(" + user['instanceCapacity'] + ")"
                ,user['instanceStayTime'])
        console.print(table)
    except:
        # 何らかの例外が発生した場合は無視して続行する
        print('error')
        time.sleep(10)
        continue