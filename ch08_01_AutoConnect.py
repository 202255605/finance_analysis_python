from pywinauto import application
import time
import os

os.system('taskkill /IM coStarter* /F /T')
os.system('taskkill /IM CpStart* /F /T')
os.system('taskkill /IM DibServer* /F /T')
os.system('wmic process where "name like \'%coStarter%\'" call terminate')
os.system('wmic process where "name like \'%CpStart%\'" call terminate')
os.system('wmic process where "name like \'%DibServer%\'" call terminate')
time.sleep(5)        

app = application.Application()
app.start('C:\CREON\STARTER\_coStarter_.exe /prj:cp /id:크레온 아이디 /pwd:[크레온 비번] /pwdcert:[내 공인인증서의 비밀번호]] /autostart')
print('오류메시지는 왜 뜨냐 결국 잘 열리고 잘 들어가지는데')
time.sleep(60)