import os, shutil, datetime
from data_parse import DataParse as dp
import json


class GainData():
    'prompt：从文件夹获取数据'

    def __init__(self):
        '''   '''
        self.addr = os.path.split(os.path.realpath(__file__))[0]  # 程序路径
        self.dmo_file_addr = self.addr + '\\' + 'DMO'
        self.addr_dmo = r'F:\DMO_upload'  # 上传dmo路径
        self.uploading_dmo_names = os.listdir(self.addr_dmo)  # 路径下要上传的DMO

    def gain(self):
        'Gain 抓取'
        # local_dmo_file = self.dmo_file_addr + '\\' + dmo_name

        for dmo in self.uploading_dmo_names:
            dmo_path = self.addr_dmo + '\\' + dmo
            shutil.copyfile(dmo_path, self.dmo_file_addr + '\\' + dmo)
            os.remove(dmo_path)

        for dmo_name in os.listdir(self.dmo_file_addr):
            dmo = self.dmo_file_addr + '\\' + dmo_name
            basic = dp(dmo_name)
            basic.addr_dmo = self.dmo_file_addr + '\\' + dmo_name
            '''
            返回两个结果，basic_info_1[0],是题头信息
            ['2018/08/25', '13:46:18', '3GG.800.709', 'VW331', 'UNTERBAU2', '34112744', '2018/08/25', '15:56:45']
                        basic_info_1[1]:是所有点的字典
                        
            '''
            basic_info_1 = basic.read_data_info()#
            # ['2018/08/25', '13:46:18', '3GG.800.709', 'VW331', 'UNTERBAU2', '34112744', '2018/08/25', '15:56:45']
            start_date = basic_info_1[0][0]  # 测量开始日期
            start_time = basic_info_1[0][1]  # 测量开始时间
            part_number = basic_info_1[0][2]  # 零件号
            vehicle_type = basic_info_1[0][3]  # 项目代号
            part_name = basic_info_1[0][4]  # 零件德语名称
            batch_number = basic_info_1[0][5]  # 零件钢号
            end_date = basic_info_1[0][6]  # 测量结束日期
            end_time = basic_info_1[0][7]  # 测量结束时间
            file_time = start_date.replace('/', '-') + ' ' + start_time

            day_date = datetime.datetime.strptime(file_time,
                                                  '%Y-%m-%d %H:%M:%S').date()
            # print(day_date)
            '按照时间进行备份'
            addr_backup = self.addr + '\\' + 'DMO_backup' + '\\' + vehicle_type + '\\' + part_name + '\\' + str(
                day_date)
            addr_dmo_backup = addr_backup + '\\' + dmo_name
            if os.path.exists(addr_backup) == False:
                os.makedirs(addr_backup)
            shutil.copyfile(dmo, addr_dmo_backup)

            os.remove(dmo)


