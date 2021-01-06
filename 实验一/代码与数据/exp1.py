import xlrd
import copy
import math


class Class(object):
    student = {}

'''学生类，用于存储学生的数据'''
class Student(object):
    id = 0
    name = ""
    sex = ""
    hometown = ""
    height = ""
    physical_test = ""
    score = []
    NULL = []                     #用于存储缺失成绩的科目号
    p_null = False

'''读取txt文件中的数据，存入一个学生类之后，再存入班级列表'''
def Load_txt(cla, filename):
    with open(filename, 'r') as f:
        next(f)
        i = 0
        for line in f.readlines():
            cla.student[i] = Student()
            (cla.student[i].id, line) = line.split(',', 1)
            (cla.student[i].name, line) = line.split(',', 1)
            (cla.student[i].hometown, line) = line.split(',', 1)
            (cla.student[i].sex, line) = line.split(',', 1)
            (cla.student[i].height, line) = line.split(',', 1)

            for j in range(0, 9):
                (s, line) = line.split(',', 1)
                try:
                    cla.student[i].score = cla.student[i].score + [int(s)]
                except:
                    '''当出现此异常时，将该成绩记为None，并将该科目号加入NULL列表'''
                    cla.student[i].score = cla.student[i].score + ['None']
                    cla.student[i].NULL = cla.student[i].NULL + [j]

            (temp, line) = line.split(',', 1)                          # 跳过score10
            (cla.student[i].physical_test, line) = line.split('\n', 1)
            if cla.student[i].physical_test == '':
                cla.student[i].p_null = True
            i += 1
        return cla, len(cla.student)

'''读取xlsx文件中的数据，存入一个学生类之后，再存入班级列表'''
def Load_excel(cla, filename, txt_len):
    length = txt_len - 1
    book = xlrd.open_workbook(filename)
    sheet = book.sheet_by_name('Sheet1')
    for row in range(1, sheet.nrows):      # 跳过第一行的表头
        col = 0
        cla.student[row+length] = Student()
        cla.student[row+length].id = sheet.cell_value(row, col)
        col += 1
        cla.student[row+length].name = sheet.cell_value(row, col)
        col += 1
        cla.student[row+length].hometown = sheet.cell_value(row, col)
        col += 1
        cla.student[row+length].sex = sheet.cell_value(row, col)
        col += 1
        cla.student[row+length].height = sheet.cell_value(row, col)

        for i in range(0, 9):
            col += 1
            if sheet.cell_value(row, col) == '':
                cla.student[row + length].score = cla.student[row + length].score + ['None']
            else:
                cla.student[row + length].score = cla.student[row + length].score + [math.trunc(sheet.cell_value(row, col))]

        col += 2          #跳过score10
        cla.student[row+length].physical_test = sheet.cell_value(row, col)

    return cla, len(cla.student) - txt_len



'''将数据格式统一'''
def data_unit(cla, txt_len, xls_len):
    '''将不规范的学号统一， 1、2、3等ID改为202001、202002、202003'''
    for i in range(0, len(cla.student)):

        #先把id的数据类型改为int类型
        cla.student[i].id = int(cla.student[i].id)

        if cla.student[i].id < 202000:
            cla.student[i].id += 202000

    '''再把数据合并，删除冗余数据'''
    for i in range(0, txt_len):
        j = txt_len
        while j < len(cla.student):
            if cla.student[i].id == cla.student[j].id:
                if cla.student[i].NULL:
                    for none_num in range(len(cla.student[i].NULL)):
                        if cla.student[j].score[(cla.student[i].NULL[none_num])] == 'None':
                            pass
                        else:
                            cla.student[i].score[cla.student[i].NULL[none_num]] = copy.deepcopy(cla.student[j].score[cla.student[i].NULL[none_num]])
                if cla.student[i].p_null == True:
                    cla.student[i].physical_test = cla.student[j].physical_test
                cla.student[j] = copy.deepcopy(cla.student[len(cla.student) - 1])
                cla.student.pop(len(cla.student) - 1)
                break
            j += 1


    '''将不规范的性别统一用male和female代替'''
    for i in range(0, len(cla.student)):
        if cla.student[i].sex == 'boy':
            cla.student[i].sex = 'male'
        if cla.student[i].sex == 'girl':
            cla.student[i].sex = 'female'

    '''将身高统一用cm作为单位'''
    for i in range(0, len(cla.student)):

        # 先把身高的数据类型改为float类型
        cla.student[i].height = float(cla.student[i].height)

        if cla.student[i].height < 10:
            cla.student[i].height *= 100

    '''将体育成绩统一'''
    for i in range(0, len(cla.student)):
        if cla.student[i].physical_test == '差':
            cla.student[i].physical_test = 'bad'
        elif cla.student[i].physical_test == '一般':
            cla.student[i].physical_test = 'general'
        elif cla.student[i].physical_test == '良好':
            cla.student[i].physical_test = 'good'
        elif cla.student[i].physical_test == '优秀':
            cla.student[i].physical_test = 'excellent'


'''第一题：求学生中家乡在Beijing的所有课程的平均成绩'''
def num_one(cla):
    #建立一个存储来自北京的学生成绩的列表
    total_score = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    num_of_Beijing = 0

    #遍历一次列表并将所有北京学生存储到新列表里
    for i in range(0, len(cla.student)):
        if(cla.student[i].hometown == 'Beijing'):
            num_of_Beijing += 1
            for j in range(9):
                total_score[j] += int(cla.student[i].score[j])

    print("----------------------------------------------------------------------")
    print("第一题：求学生中家乡在Beijing的所有课程的平均成绩")
    #打印平均成绩
    for i in range(9):
        print("课程%s的平均成绩为：%d" % (i + 1, total_score[i] / num_of_Beijing))

'''第二题：求学生中家乡在广州，课程1在80分以上，且课程9在9分以上的男同学的数量'''
def num_two(cla):
    counter = 0
    for i in range(0,len(cla.student)):
        if(cla.student[i].hometown == 'Guangzhou' and cla.student[i].sex == 'male' and int(cla.student[i].score[0]) >= 80 and int(cla.student[i].score[8]) >= 9):
            counter += 1
    print("----------------------------------------------------------------------")
    print("第二题：求学生中家乡在广州，课程1在80分以上，且课程9在9分以上的男同学的数量")
    print("符合条件的男生数量为：%d" % counter)


'''第三题：比较广州和上海两地女生的平均体能测试成绩'''
def num_three(cla):
    # 定义体育成绩所对应具体成绩的字典
    test_table = {'bad': 60, 'general': 70, 'good': 80, 'excellent': 90}

    GZ_num = 0          # 来自广州同学的人数
    GZ_ts = 0           # 来自广州同学的总分
    for i in range(0, len(cla.student)):
        if cla.student[i].hometown == 'Guangzhou':
            GZ_num += 1
            if cla.student[i].physical_test == '':
                pass
            else:
                GZ_ts += test_table[cla.student[i].physical_test]
    GZ_average = GZ_ts / GZ_num

    SH_num = 0         # 来自上海同学的人数
    SH_ts = 0          # 来自上海同学的总分
    for i in range(0, len(cla.student)):
        if cla.student[i].hometown == 'Shanghai':
            SH_num += 1
            if cla.student[i].physical_test == '':
                pass
            else:
                SH_ts += test_table[cla.student[i].physical_test]
    SH_average = SH_ts / SH_num

    print("----------------------------------------------------------------------")
    print("第三题：比较广州和上海两地女生的平均体能测试成绩")
    print("广州同学的平均体育成绩是：%f" % GZ_average)
    print("上海同学的平均体育成绩是：%f" % SH_average)

    if GZ_average > SH_average:
        print("广州同学的身体素质更强")
    elif SH_average > GZ_average:
        print("上海同学的身体素质更强")
    else:
        print("两个地方的同学身体素质不分伯仲")


'''第四题：计算学习成绩和体能测试成绩的相关性'''
def num_four(cla):
    # 定义体育成绩所对应具体成绩的字典
    test_table = {'bad': 60, 'general': 70, 'good': 80, 'excellent': 90}

    n = len(cla.student)
    sum_pt_score = 0               # 体育成绩百分制总和
    square_sum_pt = 0              # 体育成绩百分制平方和
    sum_square_pt = 0              # 体育成绩百分制和的平方
    std_pt = 0                     # 体育成绩百分制的标准差

    sum_score = [0, 0, 0, 0, 0, 0, 0, 0, 0]                # 各科成绩的总和
    square_sum_score = [0, 0, 0, 0, 0, 0, 0, 0, 0]         # 各科成绩的平方和
    sum_square_score = [0, 0, 0, 0, 0, 0, 0, 0, 0]         # 各科成绩的和平方
    average_score = [0, 0, 0, 0, 0, 0, 0, 0, 0]            # 各科成绩的平均值
    std_score = [0, 0, 0, 0, 0, 0, 0, 0, 0]                # 各科成绩的标准差
    for i in range(n):
        try:
            sum_pt_score += test_table[cla.student[i].physical_test]
            square_sum_pt += pow(test_table[cla.student[i].physical_test], 2)
        except:
            pass

        for j in range(0, 9):
            if cla.student[i].score[j] == 'None':
                pass
            else:
                sum_score[j] += cla.student[i].score[j]
                square_sum_score[j] += pow(cla.student[i].score[j], 2)

    for i in range(0, 9):
        sum_square_score[i] = pow(sum_score[i], 2)           # 求出各科成绩的和平方
        average_score[i] = sum_score[i] / n                  # 求出各科成绩的平均值

    sum_square_pt = pow(sum_pt_score, 2)                                       # 求出体育成绩的和平方
    average_pt = sum_pt_score / n                                              # 求出体育成绩的平均值
    std_pt = pow(((square_sum_pt - sum_square_pt / n) / (n - 1)), 0.5)         # 求出体育成绩的标准差

    for i in range(0, 9):
        std_score[i] = pow(((square_sum_score[i] - sum_square_score[i] / n) / (n - 1)), 0.5)     # 求出各科成绩的标准差

    # 求出各个同学体育成绩的z_score
    z_pt_score = []
    for i in range(n):
        try:
            z_pt_score.append((test_table[cla.student[i].physical_test] - average_pt) / std_pt)
        #如果无法计算则说明成绩为None，所以进行异常处理
        except:
            pass

    z_score = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0, 9):
        for j in range(n):
            try:
                z_score[i] += (((cla.student[j].score[i] - average_score[i]) / std_score[i])) * z_pt_score[j]
            except:
                pass
    for i in range(0, 9):
        z_score[i] = z_score[i] / pow(n, 0.5)

    print("----------------------------------------------------------------------")
    print("第四题：计算学习成绩和体能测试成绩的相关性")
    for i in range(0, 9):
        if z_score[i] > 0:
            p_m = '正'
        elif z_score[i] < 0:
            p_m = '负'
        else:
            p_m = '无'
        if abs(z_score[i]) > 0.8:
            relate = '高'
        elif abs(z_score[i]) > 0.6:
            relate = '中'
        elif abs(z_score[i]) > 0.4:
            relate = '低'
        else:
            relate = '无'

        print("科目%d的成绩与体育成绩的相关性p值为：%f    为%s相关，相关度%s" % (i, z_score[i], p_m, relate))



