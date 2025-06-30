from moviepy import *
from awpy import *
import polars as pl
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

def AnalyzeDemoFile():
    f = open("kill.output","w")
    dem = Demo("./example_demo/falcons-vs-vitality-m5-nuke.dem")
    dem.parse()
    
    killeventheader = dict()
    idx = 0
    for col in dem.kills.columns:
        killeventheader[col] = idx
        idx+=1
    


    
    for row in dem.kills.iter_rows():
        tick = row[killeventheader["tick"]]
        attacker_name = row[killeventheader["attacker_name"]]
        round_num = row[killeventheader["round_num"]]
        victim_name = row[killeventheader["victim_name"]]
        tsec = tick*0.015625
        min = tsec // 60
        sec = tsec % 60
        print(f"{tick},{attacker_name} => {victim_name},{min}min {sec}s,round:{round_num}")

def main():
    AnalyzeDemoFile()

if __name__ == "__main__":
    main()






