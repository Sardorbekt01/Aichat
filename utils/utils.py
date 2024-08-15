import json
from datetime import datetime, timedelta
import os

USER_DATA_FILE = 'user_data.json'
LIMITS_FILE = 'limits.json'

# Foydalanuvchi ma'lumotlarini yuklash va saqlash funksiyalari
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}
    else:
        return {}

def save_user_data(data):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

user_usage_limits = load_user_data()

def get_user_limits(user_id):
    if str(user_id) not in user_usage_limits:
        user_usage_limits[str(user_id)] = {
            "gpt3_5_limit": 0,
            "gpt4_limit": 0,
            "image_limit": 0,
            "tts_limit": 0,
            "joined_at": datetime.now().isoformat()
        }
        save_user_data(user_usage_limits)
    return user_usage_limits[str(user_id)]

# Limitlarni olish
def load_limits():
    if os.path.exists(LIMITS_FILE):
        try:
            with open(LIMITS_FILE, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {"gpt_35": 0, "gpt_4": 0, "images": 0}
    else:
        return {"gpt_35": 0, "gpt_4": 0, "images": 0}

# Statistikani hisoblash
def calculate_statistics():
    user_data = load_user_data()
    now = datetime.now()
    daily_count = weekly_count = monthly_count = yearly_count = all_time_count = 0

    for user in user_data.values():
        joined_at = datetime.fromisoformat(user["joined_at"])
        delta = now - joined_at

        if delta <= timedelta(days=1):
            daily_count += 1
        if delta <= timedelta(weeks=1):
            weekly_count += 1
        if delta <= timedelta(days=30):
            monthly_count += 1
        if delta <= timedelta(days=365):
            yearly_count += 1
        all_time_count += 1

    return {
        "daily": daily_count,
        "weekly": weekly_count,
        "monthly": monthly_count,
        "yearly": yearly_count,
        "all_time": all_time_count
    }

# Foydalanuvchi IDlarini olish
def get_all_user_ids():
    return list(load_user_data().keys())

def add_user_id_to_file(user_id):
    user_data = load_user_data()
    if str(user_id) not in user_data:
        user_data[str(user_id)] = {
            "gpt3_5_limit": 0,
            "gpt4_limit": 0,
            "image_limit": 0,
            "tts_limit": 0,
            "joined_at": datetime.now().isoformat()
        }
        save_user_data(user_data)
