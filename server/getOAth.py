import requests
import json

sid = "" # 这里写你获取到的sid 


def getUserInfo(sid: str):
	userinfo_url = "http://shixi.dfinfo.net.cn/api/user/user/bind"
	userinfo_headers = {
		"Host": "shixi.dfinfo.net.cn",
		"User-Agent": "Mozilla/5.0 (Linux; Android 12; BNE-AL00 Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Safari/537.36 MMWEBID/4997 MicroMessenger/8.0.35.2360(0x2800235D) WeChat/arm64 Weixin Android Tablet NetType/WIFI Language/zh_CN ABI/arm64",
		"X-Requested-With": "com.tencent.mm",
		"Referer": "http://shixi.dfinfo.net.cn/my",
		"Accept": "application/json, text/plain, */*",
		}
	json_data = json.loads(f'''{{"type":"wechat","sid":"{sid}","account":""}}''')
	Info = requests.post(url=userinfo_url, headers = userinfo_headers, json=json_data)
	return Info


def main():
	data = getUserInfo(sid).text
	json_data = json.loads(data)
	with open("/shixi/result.txt","w") as file:
	    file.write(data)
	    file.close()


main()
