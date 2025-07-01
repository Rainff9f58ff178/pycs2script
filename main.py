from moviepy import *
from awpy import *
import tomllib
import polars as pl
import psutil
import time
import pyautogui
import pandas as pd



with open("settings.toml", "rb") as f:
    settings = tomllib.load(f)  # 返回解析后的字典


def CutProcess():
    video1 = VideoFileClip("4月7日.mp4")  # 视频路径
    bgm1 = video1.audio
    video2 = VideoFileClip("30291986913-1-192.mp4")  # 视频路径
    bgm2 = video2.audio
    bgm2 = bgm2.with_effects([afx.AudioFadeIn("00:00:06")])

    merged_video = video1.with_audio(bgm2)

    merged_video.write_videofile(
    "输出视频.mp4", 
    codec="libx264",  # 视频编码
    audio_codec="aac"  # 音频编码
    )


def GetIdx(arr,e):
    idx = 0
    for ie in arr:
        if ie == e:
            return idx 
        idx+=1
    return -1


tick_time = 0.015625

def Tick2Time(tick):
    return tick * 0.015625

class KDTime:
    def __init__(self):
        self.tick = 0
        self.attacker_name=""
        self.victim_name=""
        self.time = ""
        self.round_num = 0    


    



class  RoundClipInfomation:
    def __init__(self):
        self.round_num = 0 
        self.role = ""
        self.killtime_infos=[]
        self.dietime_infos=[]
        self.allaction_infos=[]
    



class Context:
    def __init__(self):
        self.role_name = "5E-Player Acidia"
        self.role_player_slot = 0
        self.round_kill_info = None
        self.max_round = 0
        self.time_before_tick = 3
        self.time_later_tick = 1.5
        self.duration = self.time_before_tick + self.time_later_tick
        self.merge_time = 2.5
    
context = Context()




def AnalyzeDemoFile():
    global context
    f = open("./analyzeOutput.txt","w",encoding='utf-8')
    global settings
    dem = Demo("./demos/ancient.dem")
    dem.parse()
    
    parser = dem.parser

    max_tick = parser.parse_event("round_end")["tick"].max()
    df = parser.parse_ticks(["user_id", "team_name"], ticks=[max_tick])


    ct_players = df[df["team_name"] == "CT"]
    t_players = df[df["team_name"] == "TERRORIST"]

    ct_players = ct_players.sort_values(by="user_id")
    t_players = t_players.sort_values(by="user_id")

    all_players = pd.concat((ct_players, t_players),ignore_index=True)
    all_players.insert(0, "slot", range(1, len(all_players) + 1))

    print(all_players)
    all_players_record = all_players.to_records()
    all_players_dict = all_players.to_dict()
    headers = []
    for header in all_players_dict.keys():
        headers.append(header)
    
    for row in all_players_record:
        if row[6] == context.role_name :
            context.role_player_slot = row[3]+1
            

    print(f"{context.role_name} Spec_player {context.role_player_slot}")

    killeventheader = dict()
    idx = 0
    for col in dem.kills.columns:
        killeventheader[col] = idx
        idx+=1
    

    round_kill_info = dict()

    max_round = 0
    for row in dem.kills.iter_rows():
        tick = row[killeventheader["tick"]]
        attacker_name = row[killeventheader["attacker_name"]]
        round_num = row[killeventheader["round_num"]]
        if round_num > max_round:
            max_round = round_num
        
        victim_name = row[killeventheader["victim_name"]]
        tsec = tick*0.015625
        min = tsec // 60
        sec = tsec % 60
        # print(f"{tick},{attacker_name} => {victim_name},{min}min {sec}s,round:{round_num}")
        # if role_name == attacker_name:
        if attacker_name not in round_kill_info:
                round_kill_info[attacker_name] = dict()
        role_round_kill_info = round_kill_info[attacker_name]
        if round_num not in role_round_kill_info:
            role_round_kill_info[round_num] = RoundClipInfomation()
        rndinfo = role_round_kill_info[round_num]
        rndinfo.round_num = round_num
        rndinfo.role = attacker_name
        ktime = KDTime()
        ktime.tick = tick
        ktime.attacker_name = attacker_name
        ktime.victim_name = victim_name
        ktime.time = Tick2Time(tick)
        ktime.round_num = round_num
        rndinfo.killtime_infos.append(ktime)
        rndinfo.allaction_infos.append(ktime)

        if victim_name not in round_kill_info:
            round_kill_info[victim_name] = dict()
        role_round_kill_info = round_kill_info[victim_name]
        if round_num not in role_round_kill_info:
            role_round_kill_info[round_num] = RoundClipInfomation()
        rndinfo = role_round_kill_info[round_num]
        rndinfo.round_num = round_num
        rndinfo.role = victim_name
        ktime = KDTime()
        ktime.tick = tick
        ktime.attacker_name = attacker_name
        ktime.victim_name = victim_name
        ktime.time = Tick2Time(tick)
        ktime.round_num = round_num
        rndinfo.dietime_infos.append(ktime)
        rndinfo.allaction_infos.append(ktime)



            # print(round_num)
            # print(id(rndinfo))
            # round_kill_info[round_num] = rndinfo
    

    for k,v in round_kill_info.items():
        f.write(f"{k}:\n")
        for kk,vv in v.items():
            for vvv in vv.killtime_infos:
              print(f"round:{vvv.round_num} {vvv.attacker_name} => {vvv.victim_name} in {vvv.time} s ,tick={vvv.tick} ")
            # for vvv in vv.dietime_infos:
            #   print(f"round:{vvv.round_num} {vvv.attacker_name} => {vvv.victim_name} in {vvv.time} s ,tick={vvv.tick} ")
    context.round_kill_info = round_kill_info
    context.max_round = max_round
        
        


def is_process_running(process_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            return True
    return False



press_key_time = time.time()  # 1751344651.123456

def BeforePressKey():
    global press_key_time
    current_time = time.time()
    interval  = current_time - press_key_time
    if interval <= 0.5:
        time.sleep(0.5 - interval) 

def EndPressKey():
    press_key_time = time.time()


def GuiPressKey(key):
    BeforePressKey()
    pyautogui.keyDown(key)  # 按下回车(不释放)
    pyautogui.keyUp(key)  # 按下回车(不释放)
    EndPressKey()

def GuiTypeWrite(t):
    BeforePressKey()
    pyautogui.typewrite(t)
    EndPressKey()




def OpenConsole():
    GuiPressKey('`')
def CloseConsole():
    GuiPressKey('`')

def DemoGotoTick(tick):
    GuiTypeWrite("demo_gototick" + str(tick) )



class RecordAction:
    def __init__(self):
        self.begin_tick = 0
        self.end_tick = 0
        self.record_time= 0

    

def Time2tick(time):
    global tick_time
    return time / tick_time


def RecordOneAction(action):
    return 0
def RecordOneRound(round_kill_info):
    global context
    clips = round_kill_info.killtime_infos
    if len(clips) == 0:
        return
    record_actions =[] 
    for clip in clips:
        begin_tick = clip.tick - Time2tick(context.time_before_tick)
        end_tick = clip.tick+ Time2tick(context.time_later_tick)
        ac = RecordAction()
        ac.begin_tick = begin_tick
        ac.end_tick = end_tick
        ac.record_time = context.duration
        record_actions.append(ac)

    # merge clips 
    result_actions= []
    if(len(record_actions) == 1):
        result_actions.append(record_actions[0])

    for i in range(0,len(record_actions)-1):
        curr_rc = record_actions[i]
        next_rc = record_actions[i+1]
        diff_tick = next_rc.begin_tick - curr_rc.end_tick
        if next_rc.begin_tick <= curr_rc.end_tick or Tick2Time(diff_tick) < context.duration :
            #merge 2 rc
            new_rc = RecordAction()
            new_rc.begin_tick = curr_rc.begin_tick
            new_rc.end_tick = next_rc.end_tick
            new_rc.record_time = Tick2Time(new_rc.end_tick - new_rc.begin_tick)
            result_actions.append(new_rc)
        else:
            result_actions.append(curr_rc)
            result_actions.append(next_rc)
    output = ""
    for rc in result_actions:
        output += "{"+f"{rc.begin_tick} -> {rc.end_tick} duration= {Tick2Time(rc.end_tick-rc.begin_tick) }s" + "} "
        RecordOneAction(rc)
    print(f"round {round_kill_info.round_num}:" + output)




def Record():
    # wait_time = 3
    # while True:
    #     if is_process_running('cs2.exe'):
    #         break;
    # print("cs2.exe already boot")
    # while wait_time!=0:
    #     time.sleep(1)  # 
    #     print(str(wait_time))
    #     wait_time-=1
        
    # print("Begin Recoding ...") 
    # OpenConsole()
    # GuiTypeWrite("playdemo ancient.dem")
    # GuiPressKey('\n')
    # time.sleep(5) #等待加载
    # CloseConsole()
    global context
    role_round_kill_info = context.round_kill_info[context.role_name]

    for i in role_round_kill_info.keys():
        round_kill_info = role_round_kill_info[i]
        RecordOneRound(round_kill_info)


    return 0

def main():
    AnalyzeDemoFile()
    Record()

if __name__ == "__main__":
    main()






