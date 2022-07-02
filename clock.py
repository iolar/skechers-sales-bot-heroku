from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta
from discount_bot import fetch_data, cur_time

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=240, next_run_time=(datetime.now() + timedelta(seconds=10)))
def scheduled_worker():
    fetch_data()
    with open('result.json') as file:
        print(f'Файл {file.name} создан {cur_time}')


if __name__ == '__main__':
    sched.start()
