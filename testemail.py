#!/usr/bin/python3
 
import smtplib
from email.mime.text import MIMEText
from email.header import Header
 
# 第三方 SMTP 服务
mail_host="smtp.gmail.com"  #设置服务器
mail_user="paradox.qliphoth@gmail.com"    #用户名
mail_pass="uwdwkboghhdclyum"   #口令 
 
 
sender = 'smtp.gmail.com'
receivers = ['nanashi.owen@gmail.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
 
message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
message['From'] = Header("菜鸟教程", 'utf-8')
message['To'] =  Header("测试", 'utf-8')
 
subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')
 
 
try:
    smtpObj = smtplib.SMTP(mail_host) 
    smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(mail_user,mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    print ("success")
except smtplib.SMTPException as e:
    print(e)
    print ("Error: failed")
