import pymysql


class CreateDatabase():
    '''
    创建数据库
    创建数据库列表
    执行语句，返回数据
    执行语句，写入或者更改数据库
    '''

    def __init__(self):
        '数据库的登录信息'
        self.host = 'localhost'  # mysql的ip或者本地的地址
        self.user = 'root'  # mydql的用户
        self.pw = 'mysql-qd1'  # mysql的密码

    def logon_mysql(self, database_name=''):
        '''prompt：数据库连接
                1.inputdata:数据库名称（可选）

        '''
        db = pymysql.connect(self.host, self.user, self.pw, database_name,
                             charset='utf8')
        return db

    def create_db(self, db_name_input):
        '''prompt：创建数据库
                1.inputdata:数据库名称
                2.return：成功 Ture 失败 none
        '''
        try:
            cursor = self.logon_mysql().cursor()
            cursor.execute('show databases')
            db_names = cursor.fetchall()
            # 判断数据库是否存在
            list_dbname = []
            for db_name in db_names:
                list_dbname.append(db_name)
            if db_name_input not in list_dbname:
                cursor.execute('create database ' + db_name_input)
            return True

        except pymysql.Error as e:
            error_number = e.args[0]
            error_detail = e.args[1]
            print(f'Mysql Error{error_number}:{error_detail}')

    def create_table(self, database, table_name, table_type):
        '''prompt：创建数据列表
            1.inputdata:数据库名称,需要创建的表民称，表的格式
            2.return：成功 Ture 失败 none
            '''
        try:
            cursor = self.logon_mysql(database).cursor()
            cursor.execute('use ' + database)
            cursor.execute('show tables')
            table_names = cursor.fetchall()
            list_table = []
            for tb_name in table_names:
                list_table.append(tb_name)
            if table_name not in list_table:
                print('create tabel ' + table_name + table_type)
                cursor.execute(' CREATE TABLE ' + table_name + table_type)
                self.logon_mysql().commit()
            return True

        except pymysql.Error as e:  # 错误说明
            error_number = e.args[0]
            error_detail = e.args[1]
            print(f'Mysql Error{error_number}:{error_detail}')
            # 关闭数据库连接
            self.logon_mysql().close()

    def show_data(self, sql):
        '''prompt：执行SQL语句,返回一系列data
            1.inputdata: sql 标准语句
            2.return：语句返回的data
            '''
        try:
            cursor = self.logon_mysql().cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except:
            print("Error: SQL语句错误，或者不能匹配您的数据")

    def store_data(self, sql):
        '''prompt：执行SQL语句，将数据写入database
            1.inputdata: sql 标准语句
            2.return：按照sql语句将信息写入数据库
            '''
        try:
            cursor = self.logon_mysql().cursor()
            cursor.execute(sql)
            # 提交到数据库执行
            self.logon_mysql().commit()
        except:
            # Rollback in case there is any error
            self.logon_mysql().commit()

        # 关闭数据库连接
        self.logon_mysql().commit()

db = CreateDatabase()
db.create_db('VW331_MQB')


# tbl_name = "RO5"
# table_type = '''(PointName CHAR(50) NOT NULL primary key,
#                 X_Position FLOAT,
#                 Y_Position FLOAT,
#                 Z_Position FLOAT,
#                 i_Richtung FLOAT,
#                 j_Richtung FLOAT,
#                 k_Richtung FLOAT,
#                 UntererTol FLOAT,
#                 ObererTol FLOAT,
#                 FM_POINT  CHAR(50),
#                 CS_Statistics  CHAR(50),
#                 Characteristic  CHAR(50),
#                 Description  CHAR(50),
#                 Point_Grade  INT,
#                 Consistency  CHAR(50));
#                 '''
#
#
# tt.create_table('VW331_MQB', tbl_name, table_type)
