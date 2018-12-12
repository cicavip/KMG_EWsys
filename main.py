from gain_data import GainData
import os

'''
KMG 实时预警系统
Author:xioabin.qiu@faw-vw.com
creat_time：2018.12.7
属地布置：
    更改：init.in中，DMO_upload路径
问题：
    功能尺寸点的理论值为  0,0,0，但是其输出的FA则为其要输出的偏差 可以用。
'''
if __name__ == "__main__":
    """再此处添加一个配置文件可以在外部更改DMO上传路径"""
    file = os.path.split(os.path.realpath(__file__))[0] + "\\" + 'init.in'
    with open(file, 'r', encoding="utf-8") as f_obj:
        for line in f_obj:
            if line[0] != "#":
                info_title = line.split("=")[0]
                info = line.split("=")[1]
                if info_title  == "DMO_upload":
                    gain_data_from_file = GainData()
                    gain_data_from_file.addr_dmo = info
                    gain_data = gain_data_from_file.gain()




