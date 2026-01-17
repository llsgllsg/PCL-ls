import os
from ftplib import FTP
import sys

# FTP 上传函数
def upload_to_ftp(ftp_host, ftp_port, ftp_user, ftp_password, file_path, remote_directory):
    try:
        ftp = FTP()
        ftp.connect(ftp_host, ftp_port)
        ftp.login(user=ftp_user, passwd=ftp_password)
        
        # 切换到指定目录
        ftp.cwd(remote_directory)
        
        # 获取文件名并上传
        remote_file = os.path.basename(file_path)
        
        with open(file_path, 'rb') as file:
            ftp.storbinary(f'STOR {remote_file}', file)

        ftp.quit()
        print(f"File uploaded successfully to {remote_directory}.")
    except Exception as e:
        print(f"FTP upload failed: {e}")
        sys.exit(1)

# 更新 ini 文件函数，仅包含纯数字版本号
def update_ini_file():
    ini_file = 'main.xaml.ini'
    
    # 如果文件不存在，则创建并写入初始版本号 1
    if not os.path.exists(ini_file):
        with open(ini_file, 'w') as file:
            file.write('1')
    
    # 读取现有版本号并处理小数点情况
    with open(ini_file, 'r') as file:
        current_version = file.read().strip()
    
    # 检查是否为小数，如果是，取整数部分
    try:
        current_version = int(float(current_version))  # 将小数转换为整数
    except ValueError:
        print("Invalid version format. Resetting to 1.")
        current_version = 1

    # 版本号递增
    new_version = current_version + 1

    # 将新版本号写回文件
    with open(ini_file, 'w') as file:
        file.write(str(new_version))

    print(f"Version updated to {new_version}")

if __name__ == "__main__":
    # 更新 ini 文件
    update_ini_file()

    # 获取 FTP 相关信息
    ftp_host = 'cn-nb1.rains3.com'
    ftp_port = 8021
    ftp_user = os.getenv('FTP_USERNAME')
    ftp_password = os.getenv('FTP_PASSWORD')
    
    # 指定上传的文件夹路径
    remote_directory = '/123456'

    # 上传文件到 FTP
    upload_to_ftp(ftp_host, ftp_port, ftp_user, ftp_password, 'main.xaml.ini', remote_directory)
