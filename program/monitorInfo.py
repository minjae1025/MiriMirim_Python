from screeninfo import get_monitors

def get_physical_monitor_size():
    monitors = get_monitors()
    if monitors:
        # 일반적으로 첫 번째 모니터 정보를 가져옵니다.
        # 여러 모니터가 연결되어 있다면 for 루프를 통해 모든 모니터 정보를 확인할 수 있습니다.
        monitor = monitors[0]
        return monitor.width, monitor.height
    else:
        print("모니터를 찾을 수 없습니다.")
        return None, None

width, height = get_physical_monitor_size()