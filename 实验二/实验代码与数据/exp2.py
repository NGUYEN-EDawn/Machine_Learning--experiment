import pandas
import numpy
import matplotlib.pyplot
import seaborn
import copy
import exp1          #导入实验一的模块，方便后续读取

'''设置value的现实长度，并显示所有行和列'''
def show_value():
    pandas.set_option('display.max_columns', None)
    pandas.set_option('display.max_rows', None)
    pandas.set_option('display.max_columns', 10000)
    pandas.set_option('display.width', 10000)
    pandas.set_option('display.max_colwidth', 10000)

'''第一题：请以课程1成绩为x轴，体能成绩为y轴，画出散点图'''
def exp2_num_one(cla):
    # 定义一个体育成绩评价对应到具体成绩的字典
    test_table = {'bad': 60, 'general': 70, 'good': 80, 'excellent': 90}

    '''首先单独将类中的成绩1和体育成绩读取出来存入一个类中'''
    score1_list = []
    pt_list = []
    for i in range(len(cla.student)):
        if (cla.student[i].score[0] == 'None') or (cla.student[i].physical_test == ''):
            # 如果学生的成绩一或者体育成绩为空，则跳过该生
            pass
        else:
            score1_list.append(cla.student[i].score[0])
            pt_list.append(test_table[cla.student[i].physical_test])

    matplotlib.pyplot.scatter(score1_list, pt_list, c='green', marker='*')
    matplotlib.pyplot.title("scatter diagram")
    matplotlib.pyplot.xlabel('score1')
    matplotlib.pyplot.ylabel('physical_test')
    matplotlib.pyplot.savefig('散点图.png', bbox_inches='tight')
    matplotlib.pyplot.show()

    return score1_list       # 存储成绩1的列表第二题还要用，将其返回


'''第二题：2. 以5分为间隔，画出课程1的成绩直方图'''
def exp2_num_two(cla, score1_list):
    # 定义一个列表存储间隔
    space = [65, 70, 75, 80, 85, 90]
    matplotlib.pyplot.hist(score1_list, edgecolor='blue')
    matplotlib.pyplot.title('cube map')
    matplotlib.pyplot.grid(True, linestyle='--', alpha=0.5, axis='y')
    matplotlib.pyplot.savefig('直方图.png', dpi=300, bbox_inches='tight')
    matplotlib.pyplot.show()

'''第三题：对每门成绩进行z-score归一化，得到归一化的数据矩阵'''
def exp2_num_three(cla):
    # 定义体育成绩所对应具体成绩的字典
    test_table = {'bad': 60, 'general': 70, 'good': 80, 'excellent': 90}

    n = len(cla.student)
    sum_pt_score = 0  # 体育成绩百分制总和
    square_sum_pt = 0  # 体育成绩百分制平方和
    sum_square_pt = 0  # 体育成绩百分制和的平方
    std_pt = 0  # 体育成绩百分制的标准差

    sum_score = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # 各科成绩的总和
    square_sum_score = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # 各科成绩的平方和
    sum_square_score = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # 各科成绩的和平方
    average_score = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # 各科成绩的平均值
    std_score = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # 各科成绩的标准差
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
        sum_square_score[i] = pow(sum_score[i], 2)  # 求出各科成绩的和平方
        average_score[i] = sum_score[i] / n  # 求出各科成绩的平均值

    sum_square_pt = pow(sum_pt_score, 2)  # 求出体育成绩的和平方
    average_pt = sum_pt_score / n  # 求出体育成绩的平均值
    std_pt = pow(((square_sum_pt - sum_square_pt / n) / (n - 1)), 0.5)  # 求出体育成绩的标准差

    for i in range(0, 9):
        std_score[i] = pow(((square_sum_score[i] - sum_square_score[i] / n) / (n - 1)), 0.5)  # 求出各科成绩的标准差

    # 求出各个同学体育成绩的z_score
    z_pt_score = []
    for i in range(n):
        try:
            z_pt_score.append((test_table[cla.student[i].physical_test] - average_pt) / std_pt)
        # 如果无法计算则说明成绩为None，所以进行异常处理
        except:
            z_pt_score.append(0)

    z_score = [[] for i in range(n)]
    for i in range(0, 9):
        for j in range(n):
            try:
                z_score[j].append((cla.student[j].score[i] - average_score[i]) / std_score[i])
            except:
                z_score[j].append(0)
    for i in range(n):
        z_score[i].append(z_pt_score[i])

    matrix = numpy.mat(z_score)
    m_f = pandas.DataFrame(data=matrix)
    m_f.to_csv('z-score.txt', sep='\t', header=False, index=False)

'''第四题：计算出100x100的相关矩阵，并可视化出混淆矩阵'''
def exp2_num_four(cla):
    # 定义体育成绩所对应具体成绩的字典
    test_table = {'': 0, 'bad': 60, 'general': 70, 'good': 80, 'excellent': 90}

    # 将每个学生的所有成绩都转化成百分制
    for i in range(len(cla.student)):
        for z in range(0, 9):
            if cla.student[i].score[z] == 'None':
                cla.student[i].score[z] = 0
        for j in range(5, 9):
            cla.student[i].score[j] *= 10
        cla.student[i].physical_test = test_table[cla.student[i].physical_test]

    # 求每个学生成绩的平均值
    average_list = []
    for i in range(len(cla.student)):
        temp = 0
        un_null = 10
        for j in range(0, 9):
            if cla.student[i].score[j] == 0:
                un_null -= 1
            else:
                temp += cla.student[i].score[j]
        if cla.student[i].physical_test == 0:
            un_null -= 1
        else:
            temp += cla.student[i].physical_test
        average_list.append(temp / un_null)

    cor_mat = numpy.mat(numpy.zeros((len(cla.student), len(cla.student))))

    # 求每个学生成绩的标准差
    list_std = []
    for i in range(len(cla.student)):
        temp = 0
        un_null = 10
        for j in range(0, 9):
            if cla.student[i].score[j] == 0:
                un_null -= 1
            else:
                temp += ((cla.student[i].score[j] - average_list[i]) ** 2)
        if cla.student[i].physical_test == 0:
            un_null -= 0
        else:
            temp += ((cla.student[i].physical_test - average_list[i]) ** 2)
        list_std.append(numpy.sqrt(temp / (un_null - 1)))

    # 计算两个学生的协方差并将结果返回
    def cor(i, j):
        temp = 0
        un_null = 10
        for s in range(0, 9):
            if cla.student[i].score[s] == 0 or cla.student[j].score[s] == 0:
                un_null -= 1
            else:
                x = cla.student[i].score[s] - average_list[i]
                y = cla.student[j].score[s] - average_list[j]
                temp += (x*y)
        temp += (cla.student[i].physical_test - average_list[i]) * (cla.student[j].physical_test - average_list[j])

        return temp / (un_null - 1)

    for i in range(len(cla.student)):
        for j in range(len(cla.student)):
            t = cor(i, j)
            cor_mat[i, j] = t / (list_std[i] * list_std[j])

    matplotlib.pyplot.figure(figsize=(20, 20), dpi=80)
    seaborn.heatmap(cor_mat, vmin=-1, vmax=1, linewidths=0.08, xticklabels=False, cmap='coolwarm')  # 用热点图可视化相关矩阵
    matplotlib.pyplot.savefig('热点图.png', dpi=100, bbox_inches='tight')
    matplotlib.pyplot.show()

    return cor_mat            #将矩阵返回用于第五题

'''第五题：根据相关矩阵，找到距离每个样本最近的三个样本，得到100x3的矩阵'''
def exp2_num_five(cla, cor_mat):
    # 将传入的矩阵复制
    cor_mat_c = copy.deepcopy(cor_mat)
    maxlist = []
    id = []

    for i in range(len(cor_mat_c)):
        p = []
        l = []
        b = numpy.argsort(cor_mat_c[i], axis=1)
        p.append(cor_mat_c[i, b[0, len(cor_mat_c) - 2]])
        p.append(cor_mat_c[i, b[0, len(cor_mat_c) - 3]])
        p.append(cor_mat_c[i, b[0, len(cor_mat_c) - 4]])
        maxlist.append(p)
        l.append(cla.student[b[0, len(cor_mat_c) - 2]].id)
        l.append(cla.student[b[0, len(cor_mat_c) - 3]].id)
        l.append(cla.student[b[0, len(cor_mat_c) - 4]].id)
        id.append(l)

    id_mat = numpy.mat(id)
    dfid = pandas.DataFrame(data=id_mat)
    print(dfid)
    dfid.to_csv('矩阵输出.txt', sep='\t', index=False, header=False)


cla = exp1.Class()
cla, txt_len = exp1.Load_txt(cla, '一.数据源2-逗号间隔.txt')
cla, xls_len = exp1.Load_excel(cla, '一.数据源1.xls', txt_len)
exp1.data_unit(cla, txt_len, xls_len)
# score1_list = exp2_num_one(cla)
# exp2_num_two(cla, score1_list)
std_list = exp2_num_three(cla)
cor_mat = exp2_num_four(cla)
exp2_num_five(cla, cor_mat)