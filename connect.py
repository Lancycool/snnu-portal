import requests


account = 'xxxxxxx'
# 你的账号（学号），替换xxxxxx

password = '''xxxxxxx'''
# 你的密码，替换xxxxxxx
# 请勿将修改后的文件发给他人，以防信息泄露！

method = ''
# 默认的校园网，就不用管
# 联通填unicom
# 移动填mobile
# 电信填telecom


url = 'http://202.117.144.205:8601/snnuportal/login'
end_url = 'http://202.117.144.205:8601/snnuportal/logoff'

data = {
    'sourceurl': 'null',
    'account': account,
    'password': password,
    'yys': method,
    'issave': ''
}


headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'connection': 'keep-alive',
    'content-length': '64',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': f'JSESSIONID=A675F60D2BD910B3DEDDCB6878DD2DA6; issave=true; account={account}; password={password}',
    'host': '202.117.144.205:8601',
    'origin': 'http://202.117.144.205:8601',
    'referer': 'http://202.117.144.205:8601/snnuportal/logoff',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36'
}


response = requests.post(end_url, headers=headers).status_code
#先断开连接

response = requests.post(url, data=data, headers=headers).status_code
#请求连接

