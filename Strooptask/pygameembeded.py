import tkinter as tk
import pygame
import sys
import os
from pygame.locals import *
import subprocess
import pkg_resources
import ctypes
import numpy as np

# 사용자 설정 함수
def set_mouse_speed(speed):
    SPI_SETMOUSESPEED = 0x0071  # 마우스 속도를 설정하기 위한 SPI 코드
    ctypes.windll.user32.SystemParametersInfoA(SPI_SETMOUSESPEED, 0, speed, 0)

# 현재 마우스 속도를 가져오는 함수
def get_mouse_speed():
    SPI_GETMOUSESPEED = 0x0070  # 마우스 속도를 가져오기 위한 SPI 코드
    speed = ctypes.c_int()
    ctypes.windll.user32.SystemParametersInfoA(SPI_GETMOUSESPEED, 0, ctypes.byref(speed), 0)
    return speed.value
    
current_speed = get_mouse_speed()
print(f"Current mouse speed: {current_speed}")
# 마우스 속도를 5로 설정 (범위: 1에서 20, 기본값은 10)

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
package_names = ['pygame', 'PyAutoGUI', 'pywin32', 'pygetwindow', 'screeninfo', 'screeninfo', 'openpyxl']
for package_name in package_names:
    install_package(package_name)
    
import pygetwindow as gw
import pygame
import pyautogui
from screeninfo import get_monitors

for monitor in get_monitors():
    print(monitor)
    
def set_pygame_window_position(x, y, width, height):
    """
    Pygame window의 위치와 크기를 설정합니다.
    """
    import win32gui
    import win32con

    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, x, y, width, height, 0)
    
import pyautogui
import pygame
import random
import time
from datetime import datetime
import os
import pickle
current_path = os.getcwd()
# from datetime import datetime
import time

# base_path, trial_num = create_trial_folder(arg1)
# print("Base path set to:", base_path)


# Define colors
colors = {
    "빨강": (255, 0, 0),
    "초록": (0, 255, 0),
    "파랑": (0, 0, 255),
    "노랑": (255, 255, 0),
    "검정": (0, 0, 0),
    "하양": (255, 255, 255),
    "Neurogrin_black": (17, 17, 17),
    "Neurogrin_green": (0, 238, 205),
    "Neurogrin_gray": (207, 207, 207),
}


language = None

def run_baseline(start_time, disp="+", guide=False, \
                 screen=None, W=None, H=None, FONT_SZ=None):  # Default duration set to 30 seconds -> 30으로 추후 수정
    elapsed_time = pygame.time.get_ticks() - start_time
    
    # if elapsed_time >= duration:
    #     # 업데이트 필요 없음
    #     return False

    screen.fill(colors["Neurogrin_black"])
    font = pygame.font.SysFont('malgungothic', FONT_SZ)
    text = font.render(disp, True, colors["하양"])  # Using "+" as a fixation dot
    rect = text.get_rect(center=(int(W/2), int(H/2)))
    screen.blit(text, rect)
    
    if guide:
        # "+" 아래에 "집중해주세요." 한글 추가
        if language == 'kor': instruction_korean = font.render("십자에 집중해주세요", True, colors["하양"])
        elif language == 'eng': instruction_korean = font.render("Focus on the cross", True, colors["하양"])
        
        rect_korean = instruction_korean.get_rect(center=(int(W/2), int(H/2) + FONT_SZ * 1.3))
        screen.blit(instruction_korean, rect_korean)
        
    pygame.display.flip()

    return True

def wait_screen():
    screen.fill(colors["하양"])  # 화면을 흰색으로 채웁니다.
    font = pygame.font.SysFont('malgungothic', FONT_SZ)  # 폰트 설정
    text = font.render("클릭하여 시작합니다.", True, colors["검정"])  # 텍스트 생성
    rect = text.get_rect(center=(W/2, H/2))  # 텍스트의 위치를 화면 중앙으로 설정
    screen.blit(text, rect)  # 텍스트를 화면에 그립니다.
    pygame.display.flip()  # 화면을 갱신하여 텍스트를 표시합니다.


# Pre-generate stimuli
def generate_stimuli():
    # words = ["RED", "GREEN", "BLUE", "YELLOW"]
    if True: colors = {"빨강": (255, 0, 0), "초록": (0, 255, 0), "파랑": (0, 0, 255), "노랑": (255, 255, 0)}
    else: colors = {"RED": (255, 0, 0), "GREEN": (0, 255, 0), "BLUE": (0, 0, 255), "YELLOW": (255, 255, 0)}
    
    stimuli = {"neutral": [], "congruent": [], "incongruent": []}
    
    # neutral, match
    for color in colors:
        stimuli["neutral"].append(('XXXX', colors[color], color, True))
        
    # neutral, non-match
    for color in colors:
        for color2 in colors:
            if color != color2:
                stimuli["neutral"].append(('XXXX', colors[color], color2, False))
        
    # congruent, match
    for color in colors:
        stimuli["congruent"].append((color, colors[color], color, True))
        
    # congruent, non-match
    for color in colors:
        for color2 in colors:
            if color != color2:
                stimuli["congruent"].append((color, colors[color], color2, False))

    # incongruent, match
    for color in colors:
        for color2 in colors:
            if color != color2:
                stimuli["incongruent"].append((color, colors[color2], color2, True))
        
    # incongruent, non-match
    for color in colors:
        for color2 in colors:
            if color != color2:
                stimuli["incongruent"].append((color, colors[color2], color, False))

    return stimuli


def stimuli_중복확인(stimuli):
    # mskey = 'neutral'
    msset = []
    for mskey in stimuli:
        for i in range(len(stimuli[mskey])):
            msset.append(stimuli[mskey][i][:3])
    print(len(msset), len(set(msset)))
    print('중복 없음', len(msset) == len(set(msset)))
    
stimuli = generate_stimuli()
stimuli_중복확인(stimuli)

def 카드랜덤배정(true_ratio = 0.5): # true_ratio = 0.5 인자는 표시만 해놓음. 아직 숫자 바꿔도 적용안됨
    stimuli_selected = {"neutral": [], "congruent": [], "incongruent": []}
    
    for mskey in stimuli:
        msset_a_condition_true = []
        msset_a_condition_false = []
        for i in range(len(stimuli[mskey])):
            if stimuli[mskey][i][-1]:
                msset_a_condition_true.append(stimuli[mskey][i])
            elif not(stimuli[mskey][i][-1]):
                msset_a_condition_false.append(stimuli[mskey][i])
        """  
        경우의 수에서, True, False 각각 10개를 뽑을껀데 총 경우의수가 네개 일 경우 예외처리가 필요함.
        예외처리 대신 네개의 경우의 수를 3번 자가 중첩시켜서 12개의 경우의 수로 만들고, 
        모든 conditions 를 12개의 경우의 수로 만들어서 동일하게 처리
        """
        if len(msset_a_condition_true) == 4:
            msset_a_condition_true_duplicate = []
            for _ in range(3):
                msset_a_condition_true_duplicate += msset_a_condition_true
            msset_a_condition_true = msset_a_condition_true_duplicate
            
        print(mskey, len(msset_a_condition_true), len(msset_a_condition_false))
        
        slist = random.sample(msset_a_condition_true, 10) + random.sample(msset_a_condition_false, 10)
        random.shuffle(slist)
        stimuli_selected[mskey] = slist
        
    return stimuli_selected

if False: # 최소 생성시에만 사용
    stimuli_selected = 카드랜덤배정()
    psave2 = r'C:\\mscode\\cardsets\\cardset6.pkl'
    with open(psave2, 'wb') as file:
        pickle.dump(stimuli_selected, file)
        
def run_block(stimuli_selected, savepath=None, msid=None, screen=None, fix_x=None, fix_y=None):
    for condition in stimuli_selected:
        
        # trial = stimuli_selected[condition][0]
        for trial in stimuli_selected[condition][:1]: # 20 -> 16으로 축소
            pyautogui.move(fix_x, fix_y, duration=0)
            pygame.event.clear()

            top_word, top_color, bottom_word, is_correct = trial
    
            # Clear screen for new trial
            screen.fill(colors["Neurogrin_black"])
    
            # Display the top word in its color
            # font = pygame.font.SysFont(None, FONT_SZ)
            font = pygame.font.SysFont('malgungothic', FONT_SZ)
            top_text = font.render(top_word, True, top_color)
            top_rect = top_text.get_rect(center=(W/2, int(H/2 - (H*(1/12)))))  # Centered, adjusted for top position
            screen.blit(top_text, top_rect)
    
            pygame.display.flip()
    
            # Introduce a time gap before displaying the bottom word
            pygame.time.wait(100)  # 100 milliseconds gap as an example
            
            # Now display the bottom word (color name) in black
            bottom_text = font.render(bottom_word, True, colors["하양"])
            bottom_rect = bottom_text.get_rect(center=(W/2, int(H/2 + (H*(1/12)))))  # Centered, adjusted for bottom position
            screen.blit(bottom_text, bottom_rect)
    
            pygame.display.flip()
            cue_time_stamp = time.time()
    
            # Timing and response handling starts after displaying the bottom word
            start_time = pygame.time.get_ticks()
            response_made = False
            response = None
    
            while not response_made and (pygame.time.get_ticks() - start_time) < 1500:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        set_mouse_speed(current_speed)
                        pygame.quit()
                        quit()
                        
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:  # ESC 키를 누르면
                            set_mouse_speed(current_speed)
                            pygame.quit()
                            quit()
                        
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Left click for "Yes"
                            response = "Yes"
                            response_made = True
                        elif event.button == 3:  # Right click for "No"
                            response = "No"
                            response_made = True
    
            # Calculate response time
            response_time = pygame.time.get_ticks() - start_time if response_made else 1500

            screen.fill(colors["Neurogrin_black"])
            font = pygame.font.SysFont('malgungothic', FONT_SZ)
            text = font.render("+", True, colors["하양"])  # Using "+" as a fixation dot
            rect = text.get_rect(center=(int(W/2), int(H/2)))
            screen.blit(text, rect)
            pygame.display.flip()
            
            total_wait_time = 2000  # 1.5초의 응답 시간 + 500ms의 추가 대기 시간
            elapsed_time = pygame.time.get_ticks() - start_time  # 이미 경과한 시간
            remaining_time = total_wait_time - elapsed_time  # 남은 대기 시간 계산
            
            # 남은 대기 시간만큼 대기
            if remaining_time > 0:
                pygame.time.wait(remaining_time)

            # save_time = time.time() # msdict 저장하기 바로 전 시간 기록
            msdict = {
                'Condition': condition,
                'Top Word': top_word,
                'Top Color': top_color,
                'Bottom Word': bottom_word,
                'Response': response,
                'Correct': is_correct,
                'Response Time': response_time,
                'response_made': response_made,
                'save_time_stamp': time.time(),
                'cue_time_stamp': cue_time_stamp
                # 'nonvalid_click_time': nonvalid_click_time_saves
            }
            
            if msdict['Correct'] and msdict['Response']=='Yes': iscorrect = '맞음'
            elif not(msdict['Correct']) and msdict['Response']=='No': iscorrect = '맞음'
            elif msdict['Response'] is None: iscorrect = '응답 안함'
            else: iscorrect = '틀림'

            print('Correct', iscorrect, 'Response Time', msdict['Response Time'])

            base_path = savepath
            filename = datetime.now().strftime("%Y%m%d_%H%M%S_stroopdata.pkl")
            full_path = os.path.join(base_path, filename)
            
            # Save msdict to a file with the generated filename
            with open(full_path, 'wb') as file:
                pickle.dump(msdict, file)

from screeninfo import get_monitors
import win32gui
import win32con

def set_window_position(x, y, width, height):
    """
    지정된 위치와 크기로 Pygame 윈도우의 위치를 설정합니다.
    """
    hwnd = pygame.display.get_wm_info()['window']
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, x, y, width, height, win32con.SWP_NOZORDER)


import pyautogui
import time
from PIL import Image, ImageTk
from tkinter import font  # tkfont 대신 font로 가져옴



#%%
def resize_pygame_window(new_width, new_height):
    # Pygame display mode 변경
    screen = pygame.display.set_mode((new_width, new_height))
    
    # Tkinter 프레임 크기 변경
    embed.config(width=new_width, height=new_height)
    embed.pack_propagate(False)  # Tkinter 프레임의 크기를 강제함
    
    # Pygame 이벤트 강제 처리
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            pygame.display.update()

    # Pygame 화면 강제 업데이트
    pygame.display.flip()  # 화면의 모든 내용을 새로고침
        
import threading
def pygame_loop(W=None, H=None, FONT_SZ=None):
    pygame.init()
    # root.geometry(f"{image_width}x{image_height}")
    root.geometry(f"{W}x{H}")
    
    for widget in root.winfo_children():
        widget.destroy()

    # embed = tk.Frame(root, width=image_width, height=image_height)
    embed = tk.Frame(root, width=W, height=H)
    embed.pack(fill="both", expand=True)
    os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
    os.environ['SDL_VIDEODRIVER'] = 'windib'

    screen = pygame.display.set_mode((root.winfo_screenwidth(), root.winfo_screenheight()))
    pygame.display.set_caption("Pygame Embedded in Tkinter")

    msid = str(entry1_var.get()) #  + '_' + str(entry2_var.get())
    current_path = os.getcwd()
    now = datetime.now()
    filename = now.strftime("%Y%m%d%H%M")
    filename2 = filename + '_' + msid
    base_path_template = current_path + '\\saved_data\\' + filename2
    if not os.path.exists(base_path_template):
        os.makedirs(base_path_template)
    
    block_paths = []
    for i in range(1, 2):  # 1 to 8
        block_path = os.path.join(base_path_template, f"block{i}")
        block_paths.append(block_path)
        if not os.path.exists(block_path):
            os.makedirs(block_path)
            
        sid = entry1_var.get()
        age = entry2_var.get()
        gender = gender_var.get()
        msdict3 = {'sid': sid, 'age': age, 'gender': gender}
        
        with open(block_path + '\\idinfo.pkl', 'wb') as file:
            pickle.dump(msdict3, file)
        
    def run_pygame(arg1=None):
        running, endsw = True, False
        step = "baseline"  # baseline 단계부터 시작
        baseline_start_time = pygame.time.get_ticks()  # baseline 시작 시간 기록
        block_n = 0  # 첫 번째 블록부터 시작
        
        while running:
            current_time = pygame.time.get_ticks()  # 현재 시간
            elapsed_time = current_time - baseline_start_time  # 경과 시간
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    root.quit()
                    running = False  # 루프 종료
    
            if step == "baseline":
                # baseline이 5초 동안 유지되도록 설정
                if elapsed_time < 5000:  # 5초 동안 baseline 실행
                    run_baseline(baseline_start_time, screen=screen, W=W, H=H, FONT_SZ=FONT_SZ, guide=True)
                else:
                    # baseline이 끝났으면 다음 단계인 block으로 전환
                    step = "block"
                    block_start_time = pygame.time.get_ticks()  # block 시작 시간 기록
    
            elif step == "block":
                if block_n < 1:  # 블록 개수가 1개일 때 실행
                    # 필요한 cardset 파일 로드
                    cn = block_n + 1
                    if arg1 == 1:
                        cn += 2
                    if arg1 == 2:
                        cn += 4
    
                    global language
                    if language == 'kor': psave2 = r'utility\cardsets\cardset' + str(cn) + '.pkl'
                    elif language == 'eng': psave2 = r'utility\cardsets\cardset' + str(cn) + '_en.pkl'
                    
                    with open(psave2, 'rb') as file:
                        stimuli_selected = pickle.load(file)
    
                    fix_x, fix_y = 0, 0
    
                    # 블록 실행 (1초 동안 유지)
                    if (pygame.time.get_ticks() - block_start_time) < 3000:  # 3초 동안 실행
                        run_baseline(block_start_time, screen=screen, W=W, H=H, FONT_SZ=FONT_SZ)
                    else:
                        # 블록을 실행하고, 다음 블록 또는 종료로 넘어감
                        run_block(stimuli_selected, savepath=block_paths[block_n], msid=msid, screen=screen, fix_x=fix_x, fix_y=fix_y)
                        block_n += 1  # 다음 블록으로 이동
                        baseline_start_time = pygame.time.get_ticks()  # 다음 baseline 시작 시간
                        current_time = pygame.time.get_ticks()  # 현재 시간
                        elapsed_time = current_time - baseline_start_time  # 경과 시간
                        endsw = True
                        # step = "baseline"  # 다음 baseline으로 전환
                        
            # 모든 블록이 끝나면 종료
            if endsw:
                if elapsed_time < 3000:  # 5초 동안 baseline 실행
                    run_baseline(block_start_time, screen=screen, W=W, H=H, FONT_SZ=FONT_SZ, disp='Test end!')
                else:
                    pygame.quit()  # Quit pygame
                    running = False  # Ensure loop stops
                    main_screen_leader_board()  # Return to Tkinter main screen
                    break  # Exit the while loop completely

    # Pygame 루프를 스레드로 실행
    pygame_thread = threading.Thread(target=run_pygame, daemon=True)
    pygame_thread.start()
    
def track_mouse_position():
    # 현재 마우스 좌표 가져오기
    x, y = root.winfo_pointerx() - root.winfo_rootx(), root.winfo_pointery() - root.winfo_rooty()
    print(f"Mouse position: ({x}, {y})")

    # 1초마다 좌표를 출력
    root.after(1000, track_mouse_position)

    
def on_button_click(event, W=None, H=None, FONT_SZ=None):
    x1, y1, x2, y2 = 831, 1392, 1024, 1456
    if x1 <= event.x <= x2 and y1 <= event.y <= y2:
        print(entry1_var.get(), entry2_var.get(), gender_var.get())
        print("Button was clicked!")
        pygame_loop(W=W, H=H, FONT_SZ=FONT_SZ)

def on_button_click_first_page(event):
    global language
    x1, y1, x2, y2 = 831, 1392, 1024, 1456
    if x1 <= event.x <= x2 and y1 <= event.y <= y2:
        language = 'kor'
        on_button_click_participant_info(language=language)
        
    x1, y1, x2, y2 = 56, 1392, 239, 1456
    if x1 <= event.x <= x2 and y1 <= event.y <= y2:
        language = 'eng'
        on_button_click_participant_info(language=language)
        
background_image2 = None
def on_button_click_participant_info(language=None):
    # x1, y1, x2, y2 = 831, 1392, 1024, 1456
    # if x1 <= event.x <= x2 and y1 <= event.y <= y2:
    #     on_button_click_participant_info(language='kor')
        
    # x1, y1, x2, y2 = 56, 1392, 239, 1456
    # if x1 <= event.x <= x2 and y1 <= event.y <= y2:
    #     on_button_click_participant_info(language='eng')
        
    global background_image2  # 전역 변수로 설정
    global W, H, FONT_SZ
    global twidth, theight
    global entry1_var, entry2_var, gender_var  # 전역 변수로 설정
    global entry1, entry2, gender_frame

    print("Button was clicked!")
    # PAGE1
    rpath = r'자체디자인' + '\\'
    if language=='kor': 
        image_path = "슬라이드2.JPG"  # 이미지 경로를 설정하세요.
        man_text, woman_text = '남', '여'
    if language=='eng': 
        image_path = "슬라이드3.JPG"  # 이미지 경로를 설정하세요.
        man_text, woman_text = 'Male', 'Female'
    
    image = Image.open(rpath + image_path)
    image = image.resize((twidth, theight), Image.Resampling.LANCZOS)
    image_width, image_height = image.size
    root.geometry(f"{image_width}x{image_height}")
    background_image2 = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor="nw", image=background_image2)

    entry_font = ("Helvetica", 25, "bold")
    text_color = "#00EECD"  # 청록색
    
    gender_frame = tk.Frame(root, bg="black", width=350, height=50)
    gender_frame.place(x=450, y=1015)  # 프레임의 좌표 설정
    # label_gender = tk.Label(gender_frame, text="성별", font=label_font, fg=text_color, bg="#FFFFFF")
    # label_gender.place(x=0, y=10)  # 라벨의 좌표 설정
    gender_var = tk.StringVar()
    radio_male = tk.Radiobutton(gender_frame, text=man_text, variable=gender_var, value=man_text, font=entry_font,
                                fg=text_color, bg="black", selectcolor="#9AA5AF", indicatoron=0, width=6, height=0)
    radio_male.place(x=0, y=0)  # 좌표 및 크기 설정
    radio_female = tk.Radiobutton(gender_frame, text=woman_text, variable=gender_var, value=woman_text, font=entry_font,
                                  fg=text_color, bg="black", selectcolor="#9AA5AF", indicatoron=0, width=6, height=0)
    radio_female.place(x=150, y=0)  # 좌표 및 크기 설정
    
    # 텍스트 입력창 추가
    entry1_var = tk.StringVar()
    entry2_var = tk.StringVar()

    entry1 = tk.Entry(root, textvariable=entry1_var, font=("Helvetica", 35), width=12, bg="black", fg="white")
    entry1.place(x=452, y=814)  # 첫 번째 입력창 좌표 설정
    
    entry2 = tk.Entry(root, textvariable=entry2_var, font=("Helvetica", 35), width=12, bg="black", fg="white")
    entry2.place(x=452, y=913)  # 두 번째 입력창 좌표 설정
    canvas.bind("<Button-1>", lambda event: on_button_click_guide_page(event, language=language))
    # canvas.bind("<Button-1>", lambda event: on_button_click(event, W=W, H=H, FONT_SZ=FONT_SZ))
        
background_image_guide_page_korean = None
def on_button_click_guide_page(event, language=None):
    global W, H, FONT_SZ
    x1, y1, x2, y2 = 831, 1392, 1024, 1456
    if x1 <= event.x <= x2 and y1 <= event.y <= y2:
        global background_image_guide_page_korean  # 전역 변수로 설정
        global entry1, entry2, gender_frame  # 전역 변수로 설정해서 위젯을 삭제할 수 있게 함
        
        # 기존 위젯 삭제
        entry1.destroy()
        entry2.destroy()
        gender_frame.destroy()

        # PAGE1
        rpath = r'자체디자인' + '\\'
        if language=='kor': image_path = "슬라이드4.JPG"  # 이미지 경로를 설정하세요.
        if language=='eng': image_path = "슬라이드5.JPG"  # 이미지 경로를 설정하세요.
        
        image = Image.open(rpath + image_path)
        image = image.resize((twidth, theight), Image.Resampling.LANCZOS)
        image_width, image_height = image.size
        root.geometry(f"{image_width}x{image_height}")
        background_image_guide_page_korean = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor="nw", image=background_image_guide_page_korean)
        canvas.bind("<Button-1>", lambda event: on_button_click(event, W=W, H=H, FONT_SZ=FONT_SZ))

from screeninfo import get_monitors

def get_second_monitor_geometry():
    monitors = get_monitors()
    if len(monitors) > 1:
        second_monitor = monitors[1]  # 두 번째 모니터의 정보 가져오기
        return second_monitor.x, second_monitor.y, second_monitor.width, second_monitor.height
    else:
        return None  # 모니터가 하나만 있는 경우
second_monitor_info = get_second_monitor_geometry()

def set_fullscreen_on_second_monitor(root):
    second_monitor_info = get_second_monitor_geometry()
    if second_monitor_info:
        x, y, width, height = second_monitor_info
        # 창을 두 번째 모니터로 이동 및 크기 설정
        root.geometry(f"{width}x{height}+{x}+{y}")
        root.overrideredirect(True)  # 윈도우 창 테두리 없애고 작업 표시줄까지 덮는 설정
    else:
        print("두 번째 모니터가 없습니다.")

# Initialize Tkinter
root = tk.Tk()
root.title("Tkinter with Pygame Embedded")



if second_monitor_info:
    x, y, width, height = second_monitor_info
    root.geometry(f"{width}x{height}+{x}+{y}")  # 두 번째 모니터에서 전체 화면으로 설정
    root.state('zoomed')

    # set_fullscreen(root)
    set_fullscreen_on_second_monitor(root)

    twidth, theight = width, height
    
else:
    twidth, theight = image.width // 3, image.height // 3
    root.geometry(f"{twidth}x{theight}")


## learder board backend for PAGE1
import pandas as pd
from datetime import datetime

canvas, W, H, FONT_SZ = None, None, None, None
leader_board_img, background_image = None, None
def main_screen_leader_board():
    # PAGE1
    global leader_board_img, background_image
    global W, H, FONT_SZ
    rpath = r'자체디자인' + '\\'
    image_path = "슬라이드1.JPG"  # 이미지 경로를 설정하세요.
    leader_board_img = Image.open(rpath + image_path)
    global canvas
    
    for widget in root.winfo_children():
        widget.destroy()  # Destroy all widgets to reset the window

    leader_board_img = leader_board_img.resize((twidth, theight), Image.Resampling.LANCZOS)
    image_width, image_height = leader_board_img.size
    W, H = image_width, image_height
    FONT_SZ = int(round(46*(H/800)))
        
    background_image = ImageTk.PhotoImage(leader_board_img)
    canvas = tk.Canvas(root, width=image_width, height=image_height)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, anchor="nw", image=background_image)
    
    excel_path = r'features_output.xlsx'
    
    try:
        # 파일이 있으면 엑셀 파일 읽기
        df = pd.read_excel(excel_path)
    except FileNotFoundError:
        # 파일이 없을 경우 새로운 파일 생성
        print("파일이 존재하지 않으므로 새 파일을 생성합니다.")
        
        # 빈 데이터프레임 생성, 각 컬럼 이름을 추가
        df = pd.DataFrame({
            'date': [],
            'msid': [],
            'total_score': [],
            'netural_rt': [],
            'congruent_rt': [],
            'incongruent_rt': [],
            'netural_acc': [],
            'congruent_acc': [],
            'incongruent_acc': []
        })
        # os.makedirs(os.path.dirname(excel_path), exist_ok=True)
        df.to_excel(excel_path, index=False)
        print("새 엑셀 파일을 생성했습니다.")
    
    df = pd.read_excel(excel_path)
    
    current_date = datetime.now()
    today_msid, today_scores = [], []
    for r in range(len(df)):
        date_from_str = datetime.strptime(str(df['date'][r]), '%Y%m%d%H%M')
        istoday =  (date_from_str.year == current_date.year and 
            date_from_str.month == current_date.month and 
            date_from_str.day == current_date.day)
        
        if istoday or True:
            today_scores.append([df['total_score'][r], r,  date_from_str, df['msid'][r]])
    
    if len(today_scores) > 0:
        today_scores = np.array(today_scores)
        
        # 상위 5
        arr = np.array(today_scores[:,0], dtype=float)
        arr_no_nan = np.where(np.isnan(arr), -np.inf, arr)
        top_5_indices = np.argsort(arr_no_nan)[-5:][::-1]
        latest_index = np.argmax(today_scores[:,2])
        
        scores_disp = np.array(np.round(arr), dtype=int)
        msid_disp  = today_scores[:,3]
        
        ##
        for rown in range(len(top_5_indices)):
            # global canvas
            canvas.create_text(400, 739 + (99*rown), \
                               text=msid_disp[top_5_indices[rown]], \
                               font=("Helvetica", 30), fill="#00eecd", \
                               anchor="w")
                
            canvas.create_text(750, 739 + (99*rown), \
                               text=scores_disp[top_5_indices[rown]], \
                               font=("Helvetica", 30), fill="#00eecd", \
                               anchor="w")
             
        canvas.create_text(400, 739 + (99*5), \
                           text=msid_disp[latest_index], \
                           font=("Helvetica", 30), fill="#00eecd", \
                           anchor="w")
            
        canvas.create_text(750, 739 + (99*5), \
                           text=scores_disp[latest_index], \
                           font=("Helvetica", 30), fill="#00eecd", \
                           anchor="w")
        
    # canvas.bind("<Button-1>", on_button_click_page1)
    canvas.bind("<Button-1>", lambda event: on_button_click_first_page(event))

def img_load_update(ipath):
    global canvas, background_image  # 전역 변수로 선언
    image = Image.open(ipath)
    image = image.resize((image.width // 3, image.height // 3), Image.Resampling.LANCZOS)
    image_width, image_height = image.size
    
    for widget in root.winfo_children():
        widget.destroy()
    
    root.geometry(f"{image_width}x{image_height}")
    background_image = ImageTk.PhotoImage(image)
    
    # 기존 Canvas가 있다면 삭제
    # if canvas is not None:
    #     canvas.delete("all")
    # else:
    canvas = tk.Canvas(root, width=image_width, height=image_height)
    canvas.pack(fill="both", expand=True)
    
    canvas.create_image(0, 0, anchor="nw", image=background_image)

def button2(entrys=None):
    global user_input1, user_input2, user_input3
    user_input1 = entrys[0].get()
    user_input2 = entrys[1].get()
    user_input3 = entrys[2].get()
    print(f"입력된 이름: {user_input1}")
    print(f"입력된 생년월일: {user_input2}")
    print(f"입력된 성별: {user_input3}")
    # 여기서 추가로 수행할 동작을 추가하세요

# def on_button_click_s1_kor(): # Page2
#     print("on_button_click_s1_kor clicked!")
#     rpath = r'E:\EEG_stroop_gitmain\OpenBCI_EEGDAQ\tk' + '\\'
#     image_path = "EMC_Neurogrin_page_2_info_kor.png"  # 이미지 경로를 설정하세요.
#     ipath = rpath + image_path
#     img_load_update(ipath)

#     user_input1 = ""
#     user_input2 = ""
#     user_input3 = ""
    
#     # 텍스트 입력창 생성 및 설정
#     entry1 = tk.Entry(root, bg="#%02x%02x%02x" % (17, 17, 17), fg="#FFFFFF", borderwidth=0, highlightthickness=0)
#     custom_font = font.Font(family="Helvetica", size=28)
#     entry1.config(font=custom_font)
#     entry1.place(x=2350//3, y=1090//3, width=1200//3, height=150//3)
#     entry1.insert(0, "김뉴로")
    
#     entry2 = tk.Entry(root, bg="#%02x%02x%02x" % (17, 17, 17), fg="#FFFFFF", borderwidth=0, highlightthickness=0)
#     entry2.config(font=custom_font)
#     entry2.place(x=2350//3, y=1410//3, width=1200//3, height=150//3)
#     entry2.insert(0, "1990. 9. 1.")
    
#     entry3 = tk.Entry(root, bg="#%02x%02x%02x" % (17, 17, 17), fg="#FFFFFF", borderwidth=0, highlightthickness=0)
#     entry3.config(font=custom_font)
#     entry3.place(x=2350//3, y=1730//3, width=1200//3, height=150//3)
#     entry3.insert(0, "남자")
    
#     # 버튼 생성 및 클릭 이벤트 바인딩
#     label_button2 = tk.Label(root, image=photo2, borderwidth=0, highlightthickness=0)
#     label_button2.place(x=3000//3, y=2000//3)
#     label_button2.bind("<Button-1>", lambda e: button2(entrys=[entry1, entry2, entry3]))


    
# """
# PAGE3: stroop task 설명, 준비되면 시작
# PAGE4: pygame
# """
    
    

# Create a button in the Tkinter window




# def resize_pygame_window(new_width, new_height):
#     # Pygame display mode 변경
#     screen = pygame.display.set_mode((new_width, new_height))
    
#     # Tkinter 프레임 크기 변경
#     embed.config(width=new_width, height=new_height)
#     embed.pack_propagate(False)  # Tkinter 프레임의 크기를 강제함
    
#     # Pygame 이벤트 강제 처리
#     pygame.event.pump()  # 모든 Pygame 이벤트를 처리하여 상태를 동기화

#     # Pygame 화면 강제 업데이트
#     pygame.display.flip()  # 화면의 모든 내용을 새로고침
    
# def resize_pygame_window(new_width, new_height):
#     # Pygame display mode 변경
#     screen = pygame.display.set_mode((new_width, new_height))
    
#     # Tkinter 프레임 크기 변경
#     embed.config(width=new_width, height=new_height)
#     embed.pack_propagate(False)  # Tkinter 프레임의 크기를 강제함
    
#     # Pygame 이벤트 강제 처리
#     for event in pygame.event.get():
#         if event.type == pygame.VIDEORESIZE:
#             pygame.display.update()

#     # Pygame 화면 강제 업데이트
#     pygame.display.flip()  # 화면의 모든 내용을 새로고침



# Start the loop
# Tkinter main loop
main_screen_leader_board()
root.mainloop()
