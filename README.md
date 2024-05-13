# HtuAutoSign
  This project is focus on solve Htu Sign Problem  
  本项目致力于解决Htu所使用的智慧实习平台中签到难，打卡难，请假难的问题  
  本项目仍处于初级开发阶段，尚有许多难题亟需解决，欢迎各位积极提交issue和pr，一起让这个项目变的更好  
  目前版本号:V0.0.1 Beta

# Install
  由于本项目处于初级阶段，较难安装。。。  
  欢迎各位提交issue来完善安装教程  
  本项目共分为服务端和客户端两部分  
  服务端和客户端python版本需大于python 3.6  
  服务端和客户端均需安装requests库  
  `python3 -m pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple`  
  ## 获取sid:  
    通过对微信的抓包，获取到
    > GET http://shixi.dfinfo.net.cn/bind?data={%22userinfo%22:{%22openid%22:%22ovjve6dwytyhUfsuO2U2H_fozhYc%22,%22nickname%22:%22\u865a\u7a7a%22,%22avatar%22:%22https:\/\/thirdwx.qlogo.cn\/mmopen\/vi_32\/Q0j4TwGTfTIyNIia6IFvSwsdGuicUiaxBKjiaOrjdiaecdwnq3XbwoHpaE8fwQrhaxS323wTD27ID29Gl80icYRbUjGQ\/132%22},'sid':'BvyD64qr87CHMayPyAYKFV4uYNQTo4Z14CXGNULN'} HTTP/1.1
    如上的流量包，当然根据软件不同显示略有差距，这个包出现在他自动弹出重新登陆的时候，因此注意时机即可  
    当然也有出入，同时有可能为URL编码后的包，即出现了%22字样，实际上对应的是单引号，传参的是一个json，我这里将最后一项，也就是我们目标sid刻意改成了正常的单引号    
    请注意，你需要自己获得自己的sid，这个sid是我胡诌的，不能作为正常sid使用  
  ## 服务端：  
    服务端需要将server文件夹上传并切换到server目录下  
    修改app.py中的port端口号为自己开放的端口号  
    修改sid为自己的sid  
    并设置服务持续运行  
    例如通过screen命令创建一个新窗口，然后执行  
    `python3 app.py`  
    服务即可启动  
    然后设置定时任务定时执行getOAth.py  
    本项目建议定时30分钟  
    crontab教程这里不再赘述  
    需要注意的是，为了防止出错，定时任务中请尽可能的使用绝对路径而非相对路径来表示python3和getOAth.py
  ## 客户端:
    客户端仅需修改server_url中的地址替换为你的地址即可  
    请注意服务器默认路由为/shixi  
    这个可以不用更改，只更改ip和端口即可
  ## 额外注意：
    我们建议您服务端设置在Linux上以便使用crontab，但双端程序无论设置在何种系统都可以很好的工作

# Usage
  在最底下的main函数中  
  有is_sign和is_log  
  分别控制着是否打卡和是否提交日报  
  True为开，False为关  
  打卡需要设置经纬度信息，在main函数中修改为对应位置即可  
  日报为随机抽取，在daily目录中随机抽取一篇，需要注意后缀为txt，默认自带一篇temp.txt仅供参考  
  设置完成后，直接用python运行即可  

# Problem
  目前项目面临几个难题：  
  ## NO.1:
    首先是最难解决的项目痛点，由于智慧实习平台使用了微信小程序，其中需要利用微信鉴权  
    他的系统利用了openWeChat微信开放平台的鉴权系统  
    我们需要获取sid，才能够让系统正常工作  
    但就目前而言，sid是动态的，并且生存时间较短（1-3小时便会更新，具体时间未知）  
    本项目采取了保活机制，即使用了C/S方式，在服务器上启动一个服务，每半个小时执行一次，从而确保sid存活  
    但是这种会导致两个问题，首先是服务器部署问题，并非所有人都有公网服务器，增大了项目的实施难度  
    其次是仍然需要先捕获一个sid，而这只能通过抓包来实现，手机或者模拟器抓包又增大了入门门槛  
    这是本项目遇到的重大难题  
    开发者也尝试解决这个问题，经查阅资料，需要获取到小程序的secret key后即可获得sid  
    然而secret key未知  
    期望有人能够解决这一问题  

# TODO LIST
  将C/S双端脚本修改为可在本地运行的单端脚本，并且打包  
  将输入输出通过logging库进行美观化处理  
  实现对服务器的鉴权和分类处理  
  对WebUI实现美观化处理  
  增加更多接口处理，实现每日打卡，上传图片等  

