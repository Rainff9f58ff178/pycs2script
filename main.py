from moviepy import *
from awpy import *
import tomllib
import polars as pl

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
    


    


def AnalyzeDemoFile():
    global settings
    dem = Demo("./example_demo/falcons-vs-vitality-m5-nuke.dem")
    dem.parse()
    

    pl_names = set()
    for pl_r in dem.player_round_totals.rows():
        if pl_r[0] not in pl_names:
            pl_names.add( pl_r[0])
            print(pl_r[0])

    killeventheader = dict()
    idx = 0
    for col in dem.kills.columns:
        killeventheader[col] = idx
        idx+=1
    

    round_kill_info = dict()

    
    for row in dem.kills.iter_rows():
        tick = row[killeventheader["tick"]]
        attacker_name = row[killeventheader["attacker_name"]]
        round_num = row[killeventheader["round_num"]]
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
        print(f"{k}:")
        for kk,vv in v.items():
            # for vvv in vv.killtime_infos:
            #   print(f"round:{vvv.round_num} {vvv.attacker_name} => {vvv.victim_name} in {vvv.time} s ,tick={vvv.tick} ")
            for vvv in vv.dietime_infos:
              print(f"round:{vvv.round_num} {vvv.attacker_name} => {vvv.victim_name} in {vvv.time} s ,tick={vvv.tick} ")
        


def main():
    AnalyzeDemoFile()

if __name__ == "__main__":
    main()






