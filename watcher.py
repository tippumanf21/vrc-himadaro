import settings
import vrcpy

setting = settings.load()
client = vrcpy.Client()
print('b')
print(setting)
client.login(setting['ID'],setting['PASS'])
print('a')