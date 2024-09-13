# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 16:06:40 2024

@author: PC
"""

#%%

if False:
    import os
    # 변경할 경로
    new_path = r"E:\EEG_stroop_gitmain\OpenBCI_EEGDAQ"
    # 현재 작업 디렉토리 변경
    os.chdir(new_path)


for _ in range(2):
    try:
        import subprocess
        import pkg_resources
        import numpy as np
        import matplotlib.pyplot as plt
        from pyOpenBCI import OpenBCICyton
        import pickle
        from datetime import datetime
        import sys
        import multiprocessing
        import time
        import queue
        import os
        import auto_find_COM
        import matplotlib.image as mpimg
        break
        
    except:
        def install_package(package_name):
            # 패키지가 이미 설치되어 있는지 확인
            installed_packages = {pkg.key for pkg in pkg_resources.working_set}
            if package_name not in installed_packages:
                # 패키지가 설치되어 있지 않을 경우 설치
                subprocess.check_call(["python", "-m", "pip", "install", package_name])
                print(f"{package_name} has been installed.")
            else:
                # 패키지가 이미 설치되어 있음
                print(f"{package_name} is already installed.")
        
        # 패키지 이름 설정
        package_names = ['pyOpenBCI', 'matplotlib', 'numpy', 'xmltodict', 'pyserial', 'requests', 'pandas', 'WMI']
        for package_name in package_names:
            install_package(package_name)

#%%

current_path = os.getcwd()
plt.ion()

class MultiChannelEEGPlot:
    def __init__(self, queue, channels=[0, 1, 2], num_samples=2500, update_interval=25):
        self.queue = queue
        self.channels = channels
        self.num_samples = num_samples
        self.update_interval = update_interval
        self.data = {channel: np.zeros(self.num_samples) for channel in channels}
        
        # 배경 이미지 불러오기
        self.background_img = mpimg.imread(r'GUI_design\background_neurogrin2.png')  # 배경 이미지 파일 경로

        # 이미지 크기에 맞춰 figure 크기 설정
        img_height, img_width, _ = self.background_img.shape
        self.fig, self.axs = plt.subplots(len(channels), 1, figsize=(img_width / 100, img_height / 100))

        # 전체 figure에 배경 이미지 설정
        self.fig.figimage(self.background_img, xo=0, yo=0, zorder=-1)
        self.lines = {channel: ax.plot([], [], color)[0] for channel, ax, color in zip(
            channels, self.axs, ['#00eecd', '#7a84f2', '#c1c1c1']
        )}
        self.start_time = time.time()  # 그래프 업데이트 시작 시간 기록
        self.is_running = True  # is_running 속성을 정의
        self.update_counter = 0  # 업데이트 간격을 조절하는 카운터
        self.downsample_factor = 2  # 다운샘플링을 위한 인자

        # 축 설정 (축 정보는 필요 없으므로 축과 틱을 모두 숨깁니다)
        for ax in self.axs:
            ax.axis('off')
            
        # 각 축의 위치를 개별적으로 설정
        self.axs[0].set_position([0.017, 0.5809, 0.238, 0.2066])  # 좌뇌 그래프 위치 (left, bottom, width, height)
        self.axs[1].set_position([0.2583, 0.5809, 0.238, 0.2066])  # 우뇌 그래프 위치
        self.axs[2].set_position([0.7524, 0.5509, 0.238, 0.2066])  # 심박수 그래프 위치

        for axn in range(3):
            self.axs[axn].set_xlim(0, self.num_samples // self.downsample_factor)
            self.axs[axn].set_ylim(-8000, 8000)

    def update_plot(self):
        sample_rate = 250  # 샘플레이트, 예를 들어 250Hz
        window_size = 5 * sample_rate  # 5초간의 데이터 수, 예: 5 * 250 = 1250
        update_y_axis_interval = 5  # y축 업데이트 간격, 초 단위
        last_update_time = time.time()

        while self.is_running:
            current_time = time.time()
            try:
                data = self.queue.get_nowait()  # 큐에서 데이터 가져오기

                # 데이터를 내부 버퍼에 추가
                for channel in self.channels:
                    self.data[channel] = np.roll(self.data[channel], -1)
                    self.data[channel][-1] = data[channel]

                self.update_counter += 1
                
                if self.update_counter >= self.update_interval:
                    for channel in self.channels:
                        downsampled_data = self.data[channel][::self.downsample_factor]
                        self.lines[channel].set_data(np.arange(len(downsampled_data)), downsampled_data)
                    
                    # 매 5초마다 y축 업데이트
                    if current_time - last_update_time >= update_y_axis_interval:
                        for channel in self.channels:
                            # 최근 5초간의 데이터 선택
                            recent_data = self.data[channel][-window_size:]
                            mean = np.mean(recent_data)
                            std = np.std(recent_data)
                            lower_bound = mean - 3*std
                            upper_bound = mean + 3*std
                            self.axs[channel].set_ylim(lower_bound, upper_bound)
                        
                        last_update_time = current_time

                    self.fig.canvas.draw()
                    self.fig.canvas.flush_events()
                    self.update_counter = 0  # 카운터 리셋

            except queue.Empty:
                time.sleep(0.01)  # 큐가 비어 있으면 잠시 대기
                continue
            
    def stop(self):
        self.is_running = False

def data_collection(queue):
    callback_count = 0  # callback 함수 호출 횟수를 저장할 변수
    full_data = []  # 모든 데이터를 누적할 리스트
    start_time = None  # 첫 callback 호출 시간
    save_interval = 5  # 데이터 저장 간격 (초)
    last_save_time = time.time()  # 마지막 저장 시간

    def callback(sample):
        nonlocal callback_count, start_time, last_save_time
        if start_time is None:
            start_time = time.time()  # 첫 callback 시간 기록

        callback_count += 1

        # FPS 계산 및 출력
        current_time = time.time()
        if current_time - start_time >= 1.0:
            print(f"FPS: {callback_count}")
            callback_count = 0
            start_time = current_time

        # 샘플 데이터를 리스트로 변환하여 누적
        current_time = time.time()
        data = [sample.channels_data[channel] for channel in range(8)] + [current_time] 
        full_data.append(data)  # 누적 데이터에 추가
        queue.put(data)  # GUI 업데이트를 위해 큐에 데이터 추가
        
        if current_time - last_save_time >= save_interval:
            filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.pkl")
            filename = os.path.join(current_path, 'data', filename)
            with open(filename, 'wb') as file:
                pickle.dump(full_data, file)
                print(f"Data saved to {filename}")
                full_data.clear()  # 저장 후 데이터 클리어
            last_save_time = current_time

    try:
        with open('comnum.pkl', 'rb') as file:
            comnum = pickle.load(file)
            
        if comnum is None:
            raise ValueError('COM 포트가 None입니다.')
        
        board = OpenBCICyton(port = comnum, daisy=False)

    except:
        print('직렬포트 주소를 새로 찾습니다.')
        comnum = auto_find_COM.msmain()
        with open('comnum.pkl', 'wb') as file:
            pickle.dump(comnum, file)
        board = OpenBCICyton(port = comnum, daisy=False)
        
    # board = OpenBCICyton(port = comnum, daisy=False)
    board.start_stream(callback)

    # 데이터 수집은 사용자가 종료할 때까지 계속 실행
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        board.stop_stream()  # 사용자 인터럽트에 의해 스트림 중지
        print("Data collection finished. Exiting program.")

if __name__ == "__main__":
    data_queue = multiprocessing.Queue()
    data_process = multiprocessing.Process(target=data_collection, args=(data_queue,))

    data_process.start()

    plot = MultiChannelEEGPlot(data_queue)
    try:
        plot.update_plot()
    finally:
        plot.stop()
        data_process.join()
























































