def get_num(n):
    #     """
    #       一个圆上n个点，两两相连，可以划成多少区域
    #     """
    num = 0
    if n == 1:
        num = 1
    elif n == 2:
        num = 2
    elif n == 3:
        num = 4
    elif n > 3:
        num = rec(n, 2) + rec(n, 4) + 1
    print(num)
    return num


def rec(n, m):
    if m == n:
        return 1
    elif m == 1:
        return n
    else:
        return rec(n - 1, m - 1) + rec(n - 1, m)


def max_num(str):
    #     """
    #       给定一组非负整数，请进行拼接，
    #       得到一个最大的拼接结果。（结果可能会很大，需要返回字符串，数组长度在1到 200之间，数组中每个数的范围在[0,999999999]之间）输入•
    #       一行字符串，数字之间由逗号分隔。
    #       例如：122,10输出拼接得到的最大结果
    #       样例：输入样例1
    #           3,30,34,5,9
    #       输出样例1
    #           9534330
    #     """
    init_list = str.split(",")
    print(init_list)
    for i in range(len(init_list)):
        for j in range(i + 1, len(init_list)):
            cur_num = init_list[i]
            loop_num = init_list[j]

            cur_num_first = cur_num + loop_num
            loop_num_first = loop_num + cur_num

            if cur_num_first < loop_num_first:
                temp = loop_num
                init_list[j] = cur_num
                init_list[i] = temp
    result = ''.join(init_list)
    print(result)
    return result


def times():
    #     """
    #       给一非空的单词列表，返回前k个出现次数最多的单词。
    #       输入
    #           第一行为一个整数T(1<=T<=1000） ,表示有丁个单词，
    #           接下来是T个单词的输入，最后一行是一个整数k，表示返回需要返回前k个出现次数最多的单词
    #       输出
    #           输出k个单词，应该按单词出现频率由高到低排序。如果不同的单词有相同出现频率，按宇母顺序排序。
    #     """
    num = int(input("输入整数T(1<=T<=1000）:   "))
    words = str(input("输入T个单词:   "))
    k = int(input("输入整数k:   "))
    if len(words) != num:
        print("单词个数不对")
    else:
        target_words = words[:k]
        single_word = sorted(set(target_words))

        dict = {}
        for word in single_word:
            times = target_words.count(word)
            tempWord = ''
            for i in range(times):
                tempWord += word
            if times in dict:
                dict[times] += tempWord
            else:
                dict[times] = tempWord

        target_word = ''
        keys = list(dict.keys())
        keys.reverse()
        for key in keys:
            target_word += dict[key]
        print(target_word)
        return target_word


def num(m, n):
    #     """
    #       •给定一个闭区范围[m,n]，1<=m<=n<=10^9，求[m,nJ区间内位数为偶数的整数有多少个？
    #       •输入样例：m=1,n=100;
    #       •输出样例：90；
    #       •输出样例说明：[1,1001区间内,有10~99这些整数的位数是2,是偶数，所以答案是10-99这些整数的数量，即90;
    #       输入
    #           闭区范围[m,n]
    #     """
    target = 0
    m1 = len(str(m))
    n1 = len(str(n))
    if n1 - m1 == 0:
        target = m1 % 2 == 0 and n - m + 1 or 0
    else:
        for i in range(m1, n1):
            if i % 2 == 0:
                start = i == m1 and m or pow(10, i)
                target += (pow(10, i) - start)
                if i + 2 == n1:
                    target += n - pow(10, i + 1) + 1
                    break
            else:
                if i + 1 == n1:
                    target += n - pow(10, i) + 1
                else:
                    target += pow(10, i + 1) - pow(10, i)
    print(target)
    return target


def equal(s1: str, s2: str):
    #     """
    #       给定两个由大小写字母和空格组成的字符串 S1和$2，它们的长度都不超过 100 个字符。判断压缩掉空、并忽略大小写后，这两个字符串在是否相等。
    #       输入
    #           输入两个字符串（分两行输入)只包含字母和空格。输入有多组测试。且到文件末尾结束
    #       输出
    #           如果两个字符串相等则输出"Yes"否则输出"No”
    #     """
    str1 = s1.replace(" ", "").upper()
    str2 = s2.replace(" ", "").upper()
    if str2 == str1:
        print("Yes")
        return "Yes"
    else:
        print("No")
        return "No"


if __name__ == '__main__':
    # num = get_num(8)
    # max_num("3,30,34,5,9")
    # times()
    # num(1, 100)
    equal("er 1 2W", "er 1 2 W")
