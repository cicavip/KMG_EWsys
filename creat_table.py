from create_db import CreateDatabase
import os
import pandas as pd
import xlrd, os, xlwt


'''
根据基础数据表格。xlsx
用sql语句创建Table
project：VW3331-MQB
'''


class CrateTable():

    def __init__(self):
        self.name = "xiaobin.qiu"
        self.tabe_type = '''(PointName CHAR(50) NOT NULL primary key,
                            X_Position FLOAT,
                            Y_Position FLOAT,
                            Z_Position FLOAT,
                            i_Richtung FLOAT,
                            j_Richtung FLOAT,
                            k_Richtung FLOAT,
                            X_TOL FLOAT
                            Y_TOL FLOAT
                            Z_TOL FLOAT
                            Characteristic  CHAR(50),
                            Description  CHAR(50),
                            FM_POINT  CHAR(50),
                            FM_NAME  CHAR(50),
                            CS_Statistics  CHAR(50),
                            Consistency  CHAR(50),
                            Point_Grade  INT
                            );
                        '''
        self.xls_path = os.path.split(os.path.realpath(__file__))[
                            0] + "\\" + '01_源数据\points_info_into_db.xlsx'

    def basic_info_write_in_db(self):
        "将xls文件中的基础信息写到数据库中"
        xlsfile = xlrd.open_workbook(self.xls_path)

        canshu = (
        table, Point_Group, PointName, X_Position, Y_Position, Z_Position,
        i_Richtung, j_Richtung, k_Richtung, UntererTol, ObererTol, UntererTol_I,
        ObererTol_I, UntererTol_II, ObererTol_II, UntererTol_III, ObererTol_III,
        Characteristic, Description, Point_Grade, Consistency, FM_POINT,
        CS_Statistics)
        print(canshu)
        print(type(PointName))
        # SQL 插入语句
        sql = """INSERT INTO %s (Point_Group,PointName,X_Position,Y_Position,Z_Position,i_Richtung,j_Richtung,k_Richtung,UntererTol,
                         ObererTol,UntererTol_I,ObererTol_I,UntererTol_II,ObererTol_II,UntererTol_III,ObererTol_III,Characteristic,
                         Description, Point_Grade,Consistency,FM_POINT,CS_Statistics)
                                   VALUES (%s,'%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                                           %s,%s,%s,%s,'%s','%s',%s,'%s','%s','%s')""" % canshu
        print(sql)
        # 打开数据库连接
        db = pymysql.connect(host, user, pw, database, charset='utf8')
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # 执行sql语句
        cursor.execute(sql)

