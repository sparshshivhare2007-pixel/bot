import random
from datetime import datetime, timedelta

def random_reward(min_amt=100, max_amt=500):
    return random.randint(min_amt, max_amt)

def cooldown_passed(last_time, hours=24):
    if not last_time:
        return True
    return datetime.utcnow() - last_time > timedelta(hours=hours)
