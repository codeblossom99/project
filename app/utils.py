import shortuuid
from datetime import datetime, timedelta

def generate_short_code():
    """生成短網址"""
    return shortuuid.uuid()[:8]

def get_expiration_date(days=30):
    """得到過期日期（default == 30天）"""
    return datetime.utcnow() + timedelta(days=days)

def is_valid_url(url):
    """驗證 URL 是否可以正常work"""
    if not url.startswith(('http://', 'https://')):
        return False
    if len(url) > 2048:
        return False
    return True