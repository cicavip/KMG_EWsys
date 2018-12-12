import os
import win32api
import win32con

'''
1.返回信息：
          测量开始日期，测量开始时间，零件号，车型，零件，零件钢号，测量结束日期，测量结束时间：
          ---------------------------------------------------------------------------
        ['2018/08/25', '13:46:18', '3GG.800.709', 'VW331', 'UNTERBAU2', '34112744', '2018/08/25', '15:56:45']
2. read_data_info 中 返回 
        点的名字 point_name
        点的法向 point_direction
        点的偏差 point_deviation
        点的公差 point_tol      
        
'''


class DataParse():
    '对DMO数据进行解析'
    'prompt：dmo地址'

    def __init__(self, dmo_name):
        self.name = 'name'
        self.pro_addr = os.path.split(os.path.realpath(__file__))[0]
        self.dmo_file = self.pro_addr + '\\' + 'DMO'
        self.local_dmo_addr = self.dmo_file + '\\' + dmo_name
        self.addr_dmo = r''
        self.basic_info = []
        self.dict_point = {}

    def read_title_info(self, line):
        """
        获取DMO的基本信息： 获取零件号，车型名称缩写，零件名称缩写，零件钢号，测量结束日期，测量结束时间
        inputdata:按行读信息，基础信息
        :return: basic_info
        """
        # basic_info = []
        if line[:10] == 'PN(PARTNR)':
            self.basic_info.append(line.split("'")[1])  # 获取零件号
        elif line[:8] == 'PV(AUTO)':
            # car = line.split("'")[1]
            self.basic_info.append(line.split("'")[1])  # 获取车型名称缩写
        elif line[:10] == 'PR(PARTNM)':
            self.basic_info.append(line.split("'")[1])  # 获取零件名称缩写
        elif line[:10] == 'PS(TEILID)':
            self.basic_info.append(line.split("'")[1])  # 获取零件钢号
        elif line[:4] == 'DATE':
            self.basic_info.append(line.split(" = ")[-1])  # 测量结束日期
        elif line[:4] == 'TIME':
            self.basic_info.append(line.split(" = ")[-1])  # 测量结束时间
        else:
            pass

        return (self.basic_info)

    def read_data_info(self):
        """
        prompt
        inputdata：dmo路径，递归的基础信息
         :return 列表 basic_information: DMO的基础信息
          测量开始日期，测量开始时间，零件号，车型，零件，零件钢号，测量结束日期，测量结束时间：
          ---------------------------------------------------------------------------
        ['2018/08/25', '13:46:18', '3GG.800.709', 'VW331', 'UNTERBAU2', '34112744', '2018/08/25', '15:56:45']
        """
        with open(self.addr_dmo, 'r') as fil:
            lines = [line.strip() for line in fil]
            row_num = len(lines)
            i = 0
            while i < row_num:
                line = lines[i]
                line = line.replace("Dir1", "N")
                if len(line) > 2:
                    '''删除空行'''
                    if '，' in line:
                        line = line.replace('，', ',')

                    if line[-1] == r'$':  # 合并不同行
                        i += 1
                        line_next = lines[i]
                        line = line + line_next  # 去除末尾$
                        j = 0
                        while j < 10:  # 最多允许10个续行
                            if line_next[-1] == r'$':
                                i += 1
                                line_next = lines[i]
                                line = line + line_next
                            else:
                                break
                            j += 1
                        line = line.replace("$", "")  # 去除续行符  # 递归读取每一行
                current_row = i
                if line[
                   :3] == 'TA(' and '_abs' not in line and 'Aignment' not in line and 'Aig' not in line and 'Alignment' not in line and 'DISTB' not in line:
                    point_name = self.point_name(lines, current_row)
                    point_direction = self.point_direction(line)
                    point_deviation = self.point_deviation(line, point_name,
                                                           point_direction)
                    point_tol = self.point_tol(lines, current_row, point_name,
                                               point_direction)
                    '''将点名及偏差公差用字典存储，字典的名字不要求'''
                    list_point = [point_deviation] + point_tol
                    point_name_direction = point_name + "." + point_direction
                    dict_point = self.dict_point
                    dict_point[point_name_direction] = list_point
                read_title_info = self.read_title_info(line)

                i += 1

            return (read_title_info, dict_point)

    #
    def point_name(self, lines, current_row):
        '找到TA之后，倒叙向上查找‘FA(’，找到第一个就停止'
        try:
            for i in range(current_row, 0, -1):
                row_lookup = lines[i]
                key_1 = 'FA('
                if row_lookup[:3] == key_1:
                    point_name = row_lookup.split("(")[1].split(")")[0]
                    break  # 向上找到第一个‘FA(’就停止
            return point_name
        except:
            print("error line " + current_row)

    def point_direction(self, line):
        """
         获取评价方向
         :param line:
         :return:
         """
        point_name = line.split("(")[1].split(")")[0]
        if "." not in point_name:
            if "XAXIS" in line:
                point_direction = "X"
            elif "YAXIS" in line:
                point_direction = "Y"
            elif "ZAXIS" in line:
                point_direction = "Z"
            elif "PROFP" in line:
                point_direction = "P"
            elif "PROFS" in line:
                point_direction = "P"
            elif "NAXIS" in line:
                point_direction = "N"
            elif "WIDTH" in line and "LONG" in line:
                point_direction = "L"
            elif "WIDTH" in line and "SHORT" in line:
                point_direction = "B"
            elif "DIAM" in line:
                point_direction = "D"
            elif "TOL/POS" in line:  # 位置度偏差
                point_direction = "P"
            elif "DISTB" in line:  # 位置度偏差
                point_direction = line.split(",")[-1]
            else:
                win32api.MessageBox(0, "存在未识别的类型,该语句为：\n" + line, "错误",
                                    win32con.MB_OK | win32con.MB_ICONINFORMATION)  # 弹窗报错
            return point_direction
        else:
            point_direction = self.special_point(line, point_name)
            return point_direction

    def point_deviation(self, line, point_name, point_direction):
        '找出偏差'

        ta_point_name = line.split("(")[1].split(")")[0]
        if "." not in ta_point_name:
            point_name_direction = point_name + point_direction
        else:
            point_name_direction = point_name + "." + point_direction
        if point_name_direction == ta_point_name:
            point_deviation = line.split(",")[-2]
            return point_deviation
        else:
            win32api.MessageBox(0, "该点未找到偏差：\n" + point_name, "错误",
                                win32con.MB_OK | win32con.MB_ICONINFORMATION)

        # return point_deviation

    def point_tol(self, lines, current_row, point_name,
                  point_direction):  # '得到公差'  #     if line[2]=="T"and"TOL" in line:  #         point_tol  #  #
        '找到TA之后，倒叙向上查找‘T’，找到第一个就停止'
        try:
            # p_name_direction = point_name + point_direction
            for i in range(current_row, 0, -1):
                print(current_row)
                row_lookup = lines[i]
                key_1 = "T("
                temp_point_name = lines[current_row].split("(")[1].split(")")[0]
                if '.' not in temp_point_name:
                    p_name_direction = point_name + point_direction
                else:
                    p_name_direction = point_name + "." + point_direction
                if row_lookup[:2] == key_1:
                    tol_name_direction = row_lookup.split("(")[1].split(")")[0]
                    if tol_name_direction == p_name_direction:
                        # point_tol = point_name + "." + point_direction
                        point_tol_direction = row_lookup.split(",")[-2:]
                        break  # break  # 向上找到第一个‘FA(’就停止
                    print('current point name ' + p_name_direction)
            return point_tol_direction
        except:
            print("there is  an error in  <point_tol> and error point name is  " + point_name)

    def special_point(self, line, point_name):
        '功能尺寸点公差'

        if "XAXIS" in line:
            point_direction = point_name.split(".")[1]
        elif "YAXIS" in line:
            point_direction = point_name.split(".")[1]
        elif "ZAXIS" in line:
            point_direction = point_name.split(".")[1]
        elif "PROFP" in line:
            point_direction = point_name.split(".")[1]
        elif "PROFS" in line:
            point_direction = point_name.split(".")[1]
        elif "NAXIS" in line:
            point_direction = point_name.split(".")[1]
        elif "WIDTH" in line and "LONG" in line:
            point_direction = point_name.split(".")[1]
        elif "WIDTH" in line and "SHORT" in line:
            point_direction = point_name.split(".")[1]
        elif "DIAM" in line:
            point_direction = point_name.split(".")[1]
        elif "TOL/POS" in line:  # 位置度偏差
            point_direction = point_name.split(".")[1]
        else:
            win32api.MessageBox(0, "存在未识别的类型,该语句为：\n" + line, "错误",
                                win32con.MB_OK | win32con.MB_ICONINFORMATION)  # 弹窗报错
        return point_direction
