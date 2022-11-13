import schedule
import detect_post
from time import sleep

# schedule.every(3).minutes.do(detect_post.main)
schedule.every(30).seconds.do(detect_post.main)

while True:
    schedule.run_pending()
    sleep(1)