all = []
no = []
has = []

for i in range(1, 21):
    if i < 10:
        filename = f'2023-02-0{i}'
    else:
        filename = f'2023-02-{i}'
    with open(f'C:/Users/gs/Desktop/nodate/no_data（{filename}）.txt', encoding='utf-8') as file:
        t1_str = file.read()
        t1_str2 = t1_str.strip('[').strip(']').replace('\'', '')
        t1 = t1_str2.split(', ')
        print(len(t1))
        if i > 1:
            no = list(set(t1).intersection(set(no)))
            has = list(set(t1).union(set(has)))
        else:
            no = t1
            has = t1
        file.close()

print('无数据电表：' + str(len(no)))
print('有数据电表：' + str(len(has)))

with open('无数据电表（1-20合并）.txt', mode='w', encoding='utf-8') as file:
    file.write(str(no))
    file.close()

# with open('无数据电表（2023-02-11）.txt', encoding='utf-8') as file:
#     t2_str = file.read()
#     t1_str2 = t2_str.strip('[').strip(']').replace('\'', '')
#     t2 = t1_str2.split(', ')
#     file.close()
#
# with open('无数据电表（2023-02-12）.txt', encoding='utf-8') as file:
#     t3_str = file.read()
#     t3_str2 = t3_str.strip('[').strip(']').replace('\'', '')
#     t3 = t3_str2.split(', ')
#     file.close()
#
# t4 = list(set(t1).intersection(set(t2)))
# t5 = list(set(t3).intersection(set(t4)))
#
# print(t5)

# with open('无数据电表（三日合并）.txt', mode='w', encoding='utf-8') as file:
#     file.write(str(t5))
#     file.close()
