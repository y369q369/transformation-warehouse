import math
import time

import pandas as pd
import pymysql

medical_insurance_input = pd.read_excel('E:\download\google\medical.xlsx')
print(medical_insurance_input)
print(medical_insurance_input.values)

create_medical_insurance_sql = 'CREATE TABLE IF NOT EXISTS `medical_insurance_original_info` ( ' \
                               '`medical_id` int(8) NOT NULL AUTO_INCREMENT COMMENT \'主键id\', ' \
                               '`name` varchar(511) DEFAULT NULL COMMENT \'医保名称\', ' \
                               '`category` varchar(32) DEFAULT NULL COMMENT \'品类\', ' \
                               '`medical_type` varchar(32) DEFAULT NULL COMMENT \'医保类别\', ' \
                               '`medical_area` varchar(255) DEFAULT NULL COMMENT \'医保地区\', ' \
                               '`medical_version` varchar(255) DEFAULT NULL COMMENT \'医保版本\', ' \
                               '`reference_price` varchar(64) DEFAULT NULL COMMENT \'参考价格\', ' \
                               '`increasing_negative_ratio` varchar(32) DEFAULT NULL COMMENT \'增负比例（百分比）\', ' \
                               '`remark` varchar(1023) DEFAULT NULL COMMENT \'备注\',' \
                               '`create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT \'创建时间\', ' \
                               '`update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT \'更新时间\', ' \
                               'PRIMARY KEY (`medical_id`) ' \
                               ') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT=\'医保原始信息（手动导入）\';'
print(create_medical_insurance_sql)

truncate_medical_insurance_sql = 'TRUNCATE TABLE medical_insurance_original_info;'
print(truncate_medical_insurance_sql)

st = time.time()
insert_medical_insurance_sql = 'insert into medical_insurance_original_info(name, category, medical_type, medical_area, medical_version, reference_price, increasing_negative_ratio, remark) values '
for medical in medical_insurance_input.values:
    name = medical[1].replace('\"', '\\"')
    if isinstance(medical[8], str):
        remark = medical[8].replace('\"', '\\"')
    else:
        remark = medical[8]
    insert_medical_insurance_sql += f'\n    ("{name}", "{medical[2]}", "{medical[3]}", "{medical[4]}", "{medical[5]}", "{medical[6]}", "{medical[7]}", "{remark}"),'
insert_medical_insurance_sql = insert_medical_insurance_sql[:-1] + ';'
insert_medical_insurance_sql = insert_medical_insurance_sql.replace('nan', '')
et = time.time()
print('医保数据转换sql完成, 耗时：{} s'.format(math.ceil(et - st)))

medical_insurance_info_sql = 'drop table if exists medical_insurance_info;' \
                             'CREATE TABLE if not exists `medical_insurance_info` (' \
                             '    `medical_id` int(8) NOT NULL AUTO_INCREMENT NOT NULL COMMENT "主键id",' \
                             '    `name` varchar(511) DEFAULT NULL COMMENT "医保名称",' \
                             '    `category` varchar(255) DEFAULT NULL COMMENT "类别",' \
                             '    `medical_type` varchar(32) DEFAULT NULL COMMENT "医保类别",' \
                             '    `medical_area` varchar(255) DEFAULT NULL COMMENT "医保地区",' \
                             '    `medical_version` varchar(255) DEFAULT NULL COMMENT "医保版本",' \
                             '    `sort_code` varchar(255) DEFAULT NULL COMMENT "分类代码",' \
                             '    `reference_price` double(8,2) DEFAULT NULL COMMENT "参考价格",' \
                             '    `settle_unit_price` double(8,2) DEFAULT NULL COMMENT "核算单价",' \
                             '    `number` int(4) DEFAULT NULL COMMENT "计数",' \
                             '    `reference_deduction_percent` double(8,2) DEFAULT NULL COMMENT "参考扣除比例",' \
                             '    `settle_deduction_percent` double(8,2) DEFAULT NULL COMMENT "核算扣除比例",' \
                             '    `settle_deduction_price` double(8,2) DEFAULT NULL COMMENT "核算扣除金额",' \
                             '    `settle_price` double(8,2) DEFAULT NULL COMMENT "核算金额",' \
                             '    `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT "创建时间",' \
                             '    `create_user` varchar(255) DEFAULT NULL COMMENT "创建人",' \
                             '    `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间",' \
                             '    `update_user` varchar(0) DEFAULT NULL COMMENT "更新人",' \
                             '    PRIMARY KEY (`medical_id`)' \
                             ') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT="医保信息";' \
                             'insert into medical_insurance_info(medical_id, name, category, medical_type, medical_area, medical_version, sort_code, reference_price, number, reference_deduction_percent)' \
                             'SELECT' \
                             '    medical_id,' \
                             '    NAME,' \
                             '    category,' \
                             '    medical_type,' \
                             '    medical_area,' \
                             '    medical_version,' \
                             '    "" as sort_code,' \
                             '    NULLIF(reference_price,'') as reference_price,' \
                             '    0 as number,' \
                             '    NULLIF(increasing_negative_ratio,'') as increasing_negative_ratio' \
                             'FROM' \
                             '    medical_insurance_original_info;'

f = open('medical_insurance_original_info.sql', 'w', encoding='utf-8')
f.write(create_medical_insurance_sql)
f.write('\n\n\n\n\n')
f.write(truncate_medical_insurance_sql)
f.write('\n\n\n\n\n')
# 设置当前窗口读取大小
f.write('set global max_allowed_packet=52428800;')
f.write('\n\n\n\n\n')
f.write(insert_medical_insurance_sql)
f.write('\n\n\n\n\n')
# f.write(medical_insurance_info_sql)
f.close()

temp_conn = pymysql.connect(user='root', password='Wu5%AVGr', host='47.102.115.32', database='yq_1bxn04qa')
cursor = temp_conn.cursor()
cursor.execute(create_medical_insurance_sql)
cursor.execute(insert_medical_insurance_sql)
# cursor.execute(medical_insurance_info_sql)
temp_conn.commit()
