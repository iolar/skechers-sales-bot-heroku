from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta
from main import fetch_data, cur_time
from ftp_file_operations import ftp_send_file

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=90, next_run_time=(datetime.now() + timedelta(seconds=10)))
def scheduled_worker():
    fetch_data()
    with open('skechers.json') as file:
        print(f'Файл {file.name} создан {cur_time}')
    ftp_send_file()


if __name__ == '__main__':
    sched.start()
