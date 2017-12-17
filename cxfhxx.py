#!/usr/bin/python3
import os
import pymysql
import cx_Oracle as cx
import configparser
from pip._vendor.distlib.compat import raw_input

cf = configparser.ConfigParser()
cf.read("config.ini")
log_user = cf.get("mysqldb", "db_user")
log_pwd = cf.get("mysqldb", "db_pass")
log_host = cf.get("mysqldb", "db_host")

bsp_user = cf.get("orcaledb1", "db_user")
bsp_pwd = cf.get("orcaledb1", "db_pass")
bshost = cf.get("orcaledb1", "db_host")


def openOrcale(sql):
    conn = cx.connect(bsp_user + '/' + bsp_pwd + '@' + bshost + '/orcl')
    cursor = conn.cursor()
    cursor.execute(sql)
    row = cursor.fetchall()
    cursor.close()
    conn.close()
    return row
def serchIndex(bjbh,columnd,columnt):
        if columnd == ['']:
            columnd = ['前置库','办件库']
        for databaseName in columnd:
            if databaseName=='前置库' or databaseName == '':
                databaseName = 'HBS_QZK'
            if databaseName=='办件库' or databaseName == '':
                databaseName = 'HBS_BJK'
            for tableName in columnt:
                if tableName == "受理" or tableName == "accept" or tableName == "":
                    print("开始检索"+databaseName+"受理表.....")
                    sql = "SELECT * FROM " + databaseName +".GSB_BUSINESS_ACCEPT WHERE BJBH= '" + bjbh + "'"
                    row = openOrcale(sql)
                    if len(row) == 0:
                        print("受理表中无数据.....")
                    else:
                        print("开始输出"+databaseName+"受理表信息")
                        for r in row:
                            print(r)
                if tableName == "材料" or tableName == "file" or tableName == "":
                    print("开始检索" + databaseName + "材料表.....")
                    sql = "SELECT * FROM " + databaseName +".GSB_BUSINESS_FILES WHERE BJBH= '" + bjbh + "'"
                    row = openOrcale(sql)
                    if len(row) == 0:
                        print("材料表中无数据.....")
                    else:
                        print("开始输出" + databaseName + "材料表信息")
                        for r in row:
                            print(r)
                if tableName == "基础" or tableName == "index" or tableName == "":
                    print("开始检索" + databaseName + "基础表.....")
                    sql = "SELECT * FROM " + databaseName +".GSB_BUSINESS_INDEX WHERE BJBH= '" + bjbh + "'"
                    row = openOrcale(sql)
                    if len(row) == 0:
                        print("基础表中无数据.....")
                    else:
                        print("开始输出" + databaseName + "基础表信息")
                        for r in row:
                            print(r)
                if tableName == "流程" or tableName == "stage" or tableName == "":
                    print("开始检索" + databaseName + "流程表.....")
                    sql = "SELECT * FROM " + databaseName +".GSB_BUSINESS_STAGE WHERE BJBH= '" + bjbh + "'"
                    row = openOrcale(sql)
                    if len(row) == 0:
                        print("流程表中无数据.....")
                    else:
                        print("开始输出" + databaseName + "流程表信息")
                        for r in row:
                            print(r)
                if tableName == "特殊" or tableName == "program" or tableName == "":
                    print("开始检索" + databaseName + "特殊流程表.....")
                    sql = "SELECT * FROM " + databaseName +".GSB_BUSINESS_PROGRAM WHERE BJBH= '" + bjbh + "'"
                    row = openOrcale(sql)
                    if len(row) == 0:
                        print("特殊流程表中无数据.....")
                    else:
                        print("开始输出" + databaseName + "特殊流程表信息")
                        for r in row:
                            print(r)
                if tableName == "结果" or tableName == "result" or tableName == "":
                    print("开始检索" + databaseName + "结果表.....")
                    sql = "SELECT * FROM " + databaseName +".GSB_BUSINESS_RESULT WHERE BJBH= '" + bjbh + "'"
                    row = openOrcale(sql)
                    if len(row) == 0:
                        print("结果表中无数据.....")
                    else:
                        print("开始输出" + databaseName + "结果表信息")
                        for r in row:
                            print(r)

def serFHXX():
    if __name__ == '__main__':
        num = raw_input("请输入要查询的内容:0、退出  1、查询所有用户  2、查询对应库里所有的表  3或任意键、根据受理编码查询六张基础表是否有返回数据   ")
        if num == '0':
            os._exit(0)
        if num == '1':
            sql = "select username from all_users"
            row = openOrcale(sql)
            for r in row:
                print(r)
            serFHXX()
        if num == '2':
            user_name = raw_input("请输入要查询表的用户名:  ")
            sql = "SELECT TABLE_NAME FROM ALL_TABLES WHERE OWNER= '"+user_name+"'"
            row = openOrcale(sql)
            for r in row:
                print(r)
            serFHXX()
        if num == '3':
            bjbh = raw_input("请输入29位受理编码:  ")
            databases = raw_input("请输入需要检索的库的名字(不填则默认检索前置库+办件库):  ")
            tableNames = raw_input("请输入需要检索的表的名字(不填则默认检索全部六张基础表):  ")
            columnt = tableNames.split(',')
            columnd = databases.split(',')
            serchIndex(bjbh,columnd,columnt)

serFHXX()