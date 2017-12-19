# 综合受理数据库常用数据查询工具

import cx_Oracle as oracle_connecter
import configparser
from pip._vendor.distlib.compat import raw_input
import urllib.request as urllib_request
import requests

# 读取数据库配置项start
cf = configparser.ConfigParser()
cf.read("config.ini")
# 受理配置项
accept_user = cf.get("acceptdb", "db_user")
accept_pwd = cf.get("acceptdb", "db_pass")
accept_host = cf.get("acceptdb", "db_host")
accept_connect_str = accept_user + '/' + accept_pwd + '@' + accept_host + '/orcl'
# 审批配置项
approve_user = cf.get("approvedb", "db_user")
approve_pwd = cf.get("approvedb", "db_pass")
approve_host = cf.get("approvedb", "db_host")
approve_connect_str = approve_user + '/' + approve_pwd + '@' + approve_host + '/orcl'


# 读取数据库配置项end


# 1、查找当前业务在受理系统的状态，如果为15受理则查看是否有推送结果，如果推送成功查看审批中的业务状态
def search_accept_record(receive_number):
    # 连接受理数据库
    accept_conn = oracle_connecter.connect(accept_connect_str)
    accept_cursor = accept_conn.cursor()
    # 查询当前业务状态
    select = "select state from accept_business_index where receive_number = '" + receive_number + "'"
    accept_cursor.execute(select)
    row = accept_cursor.fetchone()
    state = row[0]
    if state == '15':
        print("业务已经受理，查询推送结果")
        # 继续查询推送结果
        select_call = "select c.call_state,r.result_value,c.called_system_addr,c.interface_name,c.parameter_value from accept_call c ,accept_call_result r  where c.CALL_ID=r.CALL_ID AND bsnum = '{}' order by c.call_time".format(receive_number)
        accept_cursor.execute(select_call)
        call_row = accept_cursor.fetchone()
        call_state = call_row[0]
        if call_state == '1':
            print("该业务已经推送成功")
        else:
            print(
                "该业务推送失败，推送结果为：{}，推送地址和参数为：{}".format(call_row[1], call_row[2] + "/" + call_row[3] + "?" + call_row[4]))
            # 查询审批数据库，确保业务没有到达审批系统，进而重新推送
            select_approve = "select state from tysp.approve_business_index where receive_number = '{}'".format(receive_number)
            accept_cursor.execute(select_approve)
            approve_row = accept_cursor.fetchone()
            if approve_row is None:
                print("审批不存在该笔业务，是否进行重新推送？")
                chance_yes_or_no = raw_input("y/n")
                if chance_yes_or_no == "y":
                    print("推送中……")
                    session = requests.session()
                    post_result = session.post(call_row[2] + "/" + call_row[3] + "?" + call_row[4])
                    print("推送成功！返回结果：{}".format(post_result.text))
    else:
        print("业务状态为：" + state)
    accept_cursor.close()
    accept_conn.close()
    link_start()


# ready?go!
def link_start():
    print("欢迎来到狂拽酷炫吊炸天的综合受理查询工具\n1-查询业务在受理系统中的状态以及接口推送情况\n")
    chance = raw_input("请选择要执行的方法：")
    if chance == '1':
        receive_number = raw_input("请输入申办流水号:")
        search_accept_record(receive_number)


# search_accept_record('11043305C2017112710050810001X')
link_start()
