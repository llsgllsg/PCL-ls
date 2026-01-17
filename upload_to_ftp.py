from ftplib import FTP
import os

# 从环境变量中获取 FTP 服务器信息
ftp_server = 'cn-nb1.rains3.com'
ftp_port = 8021
ftp_user = os.getenv('FTP_USERNAME')
ftp_pass = os.getenv('FTP_PASSWORD')

# 连接到 FTP 服务器
ftp = FTP()
ftp.connect(ftp_server, ftp_port)
ftp.login(user=ftp_user, passwd=ftp_pass)

# 切换到目标文件夹
ftp.cwd('/gf123')

# 要上传的文件路径和名称
filename = 'main.xaml'
with open(filename, 'rb') as file:
    # 上传文件
    ftp.storbinary(f'STOR {filename}', file)

# 退出 FTP 服务器
ftp.quit()

print(f'File {filename} uploaded successfully to /main')
