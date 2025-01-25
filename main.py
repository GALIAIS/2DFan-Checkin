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

            if 'error' not in result_dict:
                print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ 签到成功! 用户 Key: {key}, Session ID: {formatted_session}")
                if 'message' in result_dict:
                    print(f"   消息: {result_dict['message']}")
                if 'data' in result_dict:
                     print(f"   数据: {result_dict['data']}")

            else:
                print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ 签到失败! 用户 Key: {key}, Session ID: {formatted_session}")
                if 'message' in result_dict:
                    print(f"   错误消息: {result_dict['message']}")
                if 'error' in result_dict:
                    print(f"   详细错误: {result_dict['error']}")
                else:
                    print(f"   完整签到结果: {result_dict}")

        except Exception as e:
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🚫 签到过程中发生异常! 用户 Key: {key}, Session ID: {formatted_session}")
            print(f"   异常类型: {type(e).__name__}")
            print(f"   异常信息: {e}")

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{current_time}] 签到任务执行完成.")
