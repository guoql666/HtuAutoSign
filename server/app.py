
from http.server import HTTPServer, SimpleHTTPRequestHandler
from json import loads
import os

port = 8080 # 默认端口为8080，需要修改为你自己的
host = ('0.0.0.0', port)

class Resquest(SimpleHTTPRequestHandler):
	timeout = 5
	def do_GET(self):
		if self.path == "/shixi/token.file":
			self.send_response(200)
# 			self.send_header("Content-type","plain/text")
			self.end_headers()
			with open("./result.txt","r") as file:
				datas = loads(file.read())
				file.close()
			self.wfile.write(datas['data']['token'].encode())
		elif self.path == "/shixi/admin/reset.do":
			self.send_response(200)
			self.end_headers()
			os.popen("/usr/local/python3/bin/python3 /shixi/getOAth.py")
			self.wfile.write("success".encode())
		else:
			self.send_response(200)
			self.end_headers()
			buf = '''error'''
			self.wfile.write(buf.encode())


if __name__ == '__main__':
	print("handle start")
	server = HTTPServer(host, Resquest)
	server.serve_forever()
