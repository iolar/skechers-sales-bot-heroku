import ftplib
import json
import time
from io import BytesIO
import os

HOSTNAME = os.getenv('FTP_HOSTNAME')
USERNAME = os.getenv('FTP_USERNAME')
PASSWORD = os.getenv('FTP_PASSWORD')

ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
ftp_server.encoding = "utf-8"


def ftp_send_file(filename='skechers.json'):
    with open(filename, "rb") as file:
        ftp_server.storbinary(f"STOR /Telebots/skechers-sales-bot/{filename}", file)
    print(f'File {filename} uploaded successfully!')
    ftp_server.quit()


# def ftp_read_file(filename='skechers.json'):
#     r = BytesIO()
#     with open(filename, "r") as file:
#         ftp_server.retrbinary(f"RETR /Telebots/skechers-sales-bot/{filename}", r.write)
#     print(f'File {filename} downloaded successfully!')
#     data = r.getvalue().decode()
#     jsonData = json.loads(data)
#     return jsonData


def ftp_fetch_file(filename='skechers.json'):
    with open(filename, "wb") as file:
        ftp_server.retrbinary(f"RETR /Telebots/skechers-sales-bot/{filename}", file.write)
    print(f'File {filename} downloaded successfully!')
    ftp_server.quit()


if __name__ == '__main__':
    # ftp_send_file()
    # time.sleep(5)
    ftp_fetch_file()
