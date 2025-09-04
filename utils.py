from config import BOT_USERNAME

# ✅ Referal havola yaratish
def send_unique_invite_link(user_id: int) -> str:
    return f"https://t.me/{BOT_USERNAME}?start={user_id}"
