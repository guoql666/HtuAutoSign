import requests
from time import sleep,time
import json
import os
import random
from zhipuai import ZhipuAI

server_url = "" # 你对应的url
'''
我们假设你的ip是127.0.0.1，端口为8080
那么你这里填的应该为
server_url = "http://127.0.0.1:8080/shixi"
'''

def _getToken(): # 尝试获取token，该token不一定对
	url = server_url + "/token.file"
	data = requests.get(url)
	return data.text


def resetToken(): # 如果token 因为各种原因被重置了，由于我们服务端的保活机制，可以通过sid重新申请token
	url = server_url + "/admin/reset.do"
	data = requests.get(url)
	print("reseting")
	sleep(1) # 等待服务端请求完成并更改数据
	print(data.text)
	return _getToken()

def checkUserToken(token: str): # 判断token是否有效
	check_headers = {
		"Host": "shixi.dfinfo.net.cn",
		"User-Agent": "Mozilla/5.0 (Linux; Android 12; BNE-AL00 Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Safari/537.36 MMWEBID/4997 MicroMessenger/8.0.35.2360(0x2800235D) WeChat/arm64 Weixin Android Tablet NetType/WIFI Language/zh_CN ABI/arm64",
		"X-Requested-With": "com.tencent.mm",
		"Referer": "http://shixi.dfinfo.net.cn/my",
		"Accept": "application/json, text/plain, */*",
		"Authorization": f"Bearer {token}"
		}
	check_url = "http://shixi.dfinfo.net.cn/api/user/plan/list"
	check = requests.post(url = check_url, headers = check_headers)
	return (check.status_code == 200, check.text)


def checkPos(token: str, lat: str, lng: str): # 获取打卡位置
	check_url = "http://shixi.dfinfo.net.cn/api/plan/sign/check"
	check_headers = {
		"Host": "shixi.dfinfo.net.cn",
		"User-Agent": "Mozilla/5.0 (Linux; Android 12; BNE-AL00 Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Safari/537.36 MMWEBID/4997 MicroMessenger/8.0.35.2360(0x2800235D) WeChat/arm64 Weixin Android Tablet NetType/WIFI Language/zh_CN ABI/arm64",
		"X-Requested-With": "com.tencent.mm",
		"Referer": "http://shixi.dfinfo.net.cn/student/sign",
		"Accept": "application/json, text/plain, */*",
		"Authorization": f"Bearer {token}",
		"Content-Type": "application/json"
		}
	pos_data = {"plan_id":1001,"lat":lat,"lng":lng} 
	# pos_data = json.dumps(pos_data)
	check = requests.post(url = check_url, headers = check_headers,json = pos_data)
	return check

def sign(token: str, lat: str, lng: str, pic_url = "/upload/tmp/L68o8nyaBVJJq302XH5OpAE68S3Zb5hvQbkHXECN.jpg"): # 默认上传图片的地方，后来这儿有点小bug，后续会修复
	post_url = "http://shixi.dfinfo.net.cn/api/plan/sign/set"
	check_headers = {
		"Host": "shixi.dfinfo.net.cn",
		"User-Agent": "Mozilla/5.0 (Linux; Android 12; BNE-AL00 Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Safari/537.36 MMWEBID/4997 MicroMessenger/8.0.35.2360(0x2800235D) WeChat/arm64 Weixin Android Tablet NetType/WIFI Language/zh_CN ABI/arm64",
		"X-Requested-With": "com.tencent.mm",
		"Referer": "http://shixi.dfinfo.net.cn/student/sign",
		"Accept": "application/json, text/plain, */*",
		"Authorization": f"Bearer {token}",
		"Content-Type": "application/json"
		}
	post_data = {"plan_id":1001,"lat":lat ,"lng":lng ,"content":"","picture":[pic_url]}
	check = checkPos(token, lat, lng)
	text = json.loads(check.text)
	print(text)
	if "打卡范围内" in text['data']['notice']: # 确认打卡位置
		checkpoint_data = requests.post(url = post_url, headers = check_headers, json = post_data)
		return True,checkpoint_data.text
	elif "今日已打卡，无需重复打卡" in text['data']['notice']:
		return False,{"text":"今日已打卡，无需重复打卡","error":None}
	else:
		return (False,{"text":"error","error":"打卡失败","detail":text})

def get_random_log(): # 从daily路径中随机抽取一篇当做日报
	path = os.getcwd() + "/daily/"
	dir_list = os.listdir(path)
	dir_list = [data[0] for i in dir_list if (data:=i.split("."))[-1] == "txt"] # 获取所有以txt结尾的文本路径
	log_path = random.choices(dir_list)[0]

	with open(f"{path + log_path}.txt","r",encoding = "utf-8") as file:
		log = file.read()
		file.close()
	return log

# 这个方法用于去除字符串中的换行符
def remove_newlines(text):
    return text.replace("\n", "")

# 调用glm模型，生成日报，注意填写apikey
def generate_chat_completion():
    api_key = ""  # 请填写您自己的APIKey,智谱开发者平台里面获取。
    model = "glm-3-turbo"  # 填写需要调用的模型名称
    system_message = "你是一个大三的计算机实习生,每天都需要提交实习100字的关于当天实习内容的报告"
    user_message = "今天"

    client = ZhipuAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        stream=False,
    )
    output = response.choices[0].message.content
    return remove_newlines(output)

def log(token: str):
	log_url = "http://shixi.dfinfo.net.cn/api/plan/daily/set"
	log_headers = {
		"Host": "shixi.dfinfo.net.cn",
		"User-Agent": "Mozilla/5.0 (Linux; Android 12; BNE-AL00 Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Safari/537.36 MMWEBID/4997 MicroMessenger/8.0.35.2360(0x2800235D) WeChat/arm64 Weixin Android Tablet NetType/WIFI Language/zh_CN ABI/arm64",
		"X-Requested-With": "com.tencent.mm",
		"Referer": "http://shixi.dfinfo.net.cn/student/daily",
		"Accept": "application/json, text/plain, */*",
		"Authorization": f"Bearer {token}",
		"Content-Type": "application/json"
		}

	# log = get_random_log()
	log = generate_chat_completion()
	date_time = int(time()//86400 * 86400 - 28800) # 86400是一天时间，由于时间是从1970年1月1日8点计算，因此减去8小时偏移量，得到当日零点时间戳
	log_data = {"plan_id":1001,"time":[str(date_time)],"content":log}
	log_post = requests.post(url = log_url, headers = log_headers, json = log_data)
	return (log_post.status_code == 200, json.loads(log_post.text))

def is_daily_log() -> bool: # 确保一天只提交一次日报，避免重复提交
	pass



def getToken() -> str:
	token = _getToken()
	check = checkUserToken(token)
	if check[0] == False:
		token = resetToken()
	check = checkUserToken(token)
	if check[0] == False:
		raise EOFError("Can`t connect with server data")
	return token

def main():
	is_sign = True
	is_log = True
  # 经纬度需要换为你需要打卡的地方的值，这个可以在第一次抓包sid的时候顺带搞到，也可以通过其他软件获取
	lat = "34.842884" # 经度
	lng = "113.73667" # 纬度
	token = getToken()
	if is_sign:
		print(sign(token,lat,lng))
	if is_log:
		print(log(token))

if __name__ == "__main__":
	main()
