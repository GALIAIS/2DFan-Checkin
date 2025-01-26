import json
import os
from typing import Optional
from api import User
from recaptcha import EzCaptchaImpl
import datetime

session_map_str: Optional[str] = os.environ.get(key='SESSION_MAP', default=None)
if not session_map_str:
    raise EnvironmentError("缺少环境变量 SESSION_MAP。请设置 SESSION_MAP 环境变量，其值为 JSON 格式的 session 字典。")

try:
    session_map: dict[str, str] = json.loads(session_map_str)
except json.JSONDecodeError:
    raise EnvironmentError("环境变量 SESSION_MAP JSON 格式解析失败。请检查 SESSION_MAP 环境变量是否为有效的 JSON 字符串。")

http_proxy: Optional[str] = os.environ.get(key='HTTP_PROXY', default=None)

def format_session_id(session: str, length: int = 3) -> str:
    """格式化显示 session ID，只显示前几位以脱敏，并增加可读性"""
    if not session:
        return "<empty session>"
    return session[:length] + "***" if len(session) > length else session
if __name__ == '__main__':
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] 开始执行签到任务...")

    for key, session in session_map.items():
        formatted_session = format_session_id(session)
        print(f"\n[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 用户 Key: {key}, Session ID: {formatted_session}  开始签到...")
        user = User(key, session, EzCaptchaImpl())
        if http_proxy:
            user.session.proxies.update({
                'http': http_proxy,
                'https': http_proxy,
            })
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 使用代理: {http_proxy}")

        try:
            checkin_result = user.checkin()
            result_dict = checkin_result.__dict__

            if 'checkins_count' in result_dict and 'serial_checkins' in result_dict:
                print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ 签到成功! 用户 Key: {key}, Session ID: {formatted_session}")
                print(f"   累计签到次数: {result_dict['checkins_count']}")
                print(f"   连续签到天数: {result_dict['serial_checkins']}")


            else:
                print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ 签到失败! 用户 Key: {key}, Session ID: {formatted_session}")
                print(f"   信息: {result_dict}")

        except Exception as e:
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🚫 签到过程中发生异常! 用户 Key: {key}, Session ID: {formatted_session}")
            print(f"   异常类型: {type(e).__name__}")
            print(f"   异常信息: {e}")

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{current_time}] 签到任务执行完成.")
