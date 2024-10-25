import matplotlib.pyplot as plt
import numpy as np
def write_res(data_path, des_path, thresholds_file_path_RF16, thresholds_file_path_RF11, have_TMB = False):
    """
    在data_path中新添两列或三列，标明RF16模型、RF11模型和TMB预测各样本是R还是NR。
    如果RF16模型给出的预测值(RF16_prob)≥阈值，就说明模型预测该样本为R（应答者），否则为NR（非应答者）；
    如果TMB≥10，则根据TMB的预测结果为R，否则为NR。
    have_TMB为False时，使用泛癌模型（使用全部癌症种类构建的），反之使用癌症特异性模型（根据不同癌症模型预测不同癌症的患者）
    :param data_path: Training_RF_Prob/Test_RF_Prob
    :param des_path: 文件输出路径
    :param thresholds_file_path_RF16: Pan_Thresholds/Thresholds
    :param thresholds_file_path_RF11: Pan_Thresholds_RF11/Thresholds_RF11
    :param have_TMB: 是否根据TMB预测
    """
    def isfloat(n):  # 文件中的某行是不是数字
        try:
            float(n)
        except:
            return False
        return True
    def get_cutoff(thresholds_file_path):  # 从文件中读取阈值
        rf = open(thresholds_file_path, 'r')
        line = rf.readline()
        cutoff = []  # 是前面得到的最佳阈值
        flag = False
        while line != '':
            line = line.split()
            if flag and isfloat(line[0]):
                cutoff.append(round(float(line[0]), 3))
                flag = False
            if not isfloat(line[0]):
                flag = True
            line = rf.readline()
        rf.close()
        return cutoff
    cutoff_RF16 = get_cutoff(thresholds_file_path_RF16)
    cutoff_RF11 = get_cutoff(thresholds_file_path_RF11)
    rf = open(data_path, 'r')
    wf = open(des_path, 'w')  # 结果写入到这个文件
    line = rf.readline()
    while line != '':
        line = line.strip().split('\t')
        if line[0] == 'Sample_ID':  # 如果是第一行（列名），就直接写入文件中作为列名
            wf.write('\t'.join(line) + '\t' + 'RF16' + '\t' + 'RF11' + (('\t' + 'TMB_10') if have_TMB else "") + '\n')
        else:
            cancer_type = int(line[1]) if have_TMB else 0  # 如果是特异性模型，就根据每个样本的癌症种类选择对应的癌症模型阈值
            RF16_res = ('\t' + "R") if float(line[-2]) >= cutoff_RF16[cancer_type] else ('\t' + "NR")
            RF11_res = ('\t' + "R") if float(line[-1]) >= cutoff_RF11[cancer_type] else ('\t' + "NR")
            TMB10_res = (('\t' + "R") if float(line[-3]) >= float(10) else ('\t' + "NR")) if have_TMB else ""
            wf.write('\t'.join(line) + RF16_res + RF11_res + TMB10_res + '\n')
        line = rf.readline()
    rf.close()
    wf.close()

'''
# 泛癌模型预测结果--训练组
write_res('data/Training_RF_Prob.txt', 'data/Training_RF_Prob_Pan_Predicted.txt', '../r/data/Pan_Thresholds.txt', '../r/data/Pan_Thresholds_RF11.txt', False)
# 癌症特异模型预测结果--训练组
write_res('data/Training_RF_Prob.txt', 'data/Training_RF_Prob_Predicted.txt', '../r/data/Thresholds.txt', '../r/data/Thresholds_RF11.txt', True)
# 癌症特异模型预测结果--验证组
write_res('data/Test_RF_Prob.txt', 'data/Test_RF_Prob_Predicted.txt', '../r/data/Thresholds.txt', '../r/data/Thresholds_RF11.txt', True)
'''

def evaluation(data_path, target, round_num = -1, is_print = True):
    """
    根据上面的预测结果，计算并输出各模型对各种癌症的预测灵敏度、特异性、准确率、阳/阴性预测值
    :param data_path: 上面得到的预测结果文件。
    :param target: 根据倒数第几列计算--在有TMB的文件中，-1为TMB、-2为RF16；没有TMB时只能取-1，即RF16
    :param round_num: 保留几位小数，默认不进行四舍五入
    :param is_print: 是否在控制台打印结果
    :return: 返回一个二元元组，第一个值为一个一维数组，为泛癌和3中特异性癌症的灵敏度、特异性、准确率、阳/阴性预测值；第二个值为一个二维数组，其中每个子数组为泛癌和3中特异性癌症的tp、tn、fp、fn值
    """
    def show_res(tp, tn, fp, fn, is_print):  # 计算灵敏度、特异性、准确率、阳/阴性预测值，并print
        if is_print:
            print("tn:" + str(tn) + '\t' + "fp:" + str(fp) + '\n' + "fn:" + str(fn) + '\t' + "tp:" + str(tp))
        sensitivity = float(tp) / (float(tp + fn)) * 100
        specificity = float(tn) / (float(fp + tn)) * 100
        accuracy = float(tp + tn) / (float(tp + fp + fn + tn)) * 100
        ppv = float(tp) / (float(tp + fp)) * 100
        npv = float(tn) / (float(fn + tn)) * 100
        res = [sensitivity, specificity, accuracy, ppv, npv]
        if round != -1:
            sensitivity, specificity, accuracy, ppv, npv = round(sensitivity, round_num), round(specificity, round_num), round(accuracy, round_num), round(ppv, round_num), round(npv, round_num)
        if is_print:
            print("sensitivity:" + str(sensitivity) + '\n' + "specificity:" + str(specificity) + '\n' + "accuracy:" + str(accuracy) + '\n' + "ppv:" + str(ppv) + '\n' + "npv:" + str(npv) + '\n')
        return res
    order = ['Melanoma', 'NSCLC', 'Others']  # 按这个顺序进行计算
    tp, tn, fp, fn = [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]  # 这里不能写成tp=tn=[0,0,0]，这样这几个数组指向同一个列表，值都相等
    rf = open(data_path, 'r')
    line = rf.readline().strip().split('\t')
    while line[0] != '':
        if line[0] != 'Sample_ID':  # 如果不是列名的那行
            index = int(line[1])
            if line[2] == '1':  # 样本实际为正类
                if line[target] == 'R':  # 预测也为正类--tp
                    tp[index] += 1
                else:  # 预测为负类--fn
                    fn[index] += 1
            else:  # 样本实际为负类
                if line[target] == 'R':  # 预测为正类--fp
                    fp[index] += 1
                else:  # 预测也为负类--tn
                    tn[index] += 1
        line = rf.readline().strip().split('\t')
    rf.close()
    m_n_o_res = []
    res = []
    res_tptnfpfn = []
    for i in range(len(order)):
        if is_print:
            print(order[i] + ":")
        res_tptnfpfn.append([tp[i], tn[i], fp[i], fn[i]])
        m_n_o_res.extend(show_res(tp[i], tn[i], fp[i], fn[i], is_print))
    if is_print:
        print('Pan-cancer total res:')
    res.extend(show_res(sum(tp), sum(tn), sum(fp), sum(fn), is_print))
    res.extend(m_n_o_res)
    res_tptnfpfn.insert(0, [sum(tp), sum(tn), sum(fp), sum(fn)])
    return res, res_tptnfpfn

'''
print('训练组--泛癌模型预测结果')
evaluation('data/Training_RF_Prob_Pan_Predicted.txt', -2, 2, False)
print("\n")
print('训练组--特异性模型预测结果')
evaluation('data/Training_RF_Prob_Predicted.txt', -3, 2, False)
print("\n")
print('训练组--TMB预测结果')
evaluation('data/Training_RF_Prob_Predicted.txt', -1, 2, False)
print("\n")
'''
# print('验证组--特异性模型预测结果')
rf16, rf16_tptnfpfn = evaluation('data/Test_RF_Prob_Predicted.txt', -3, 2, False)
# print("\n")
# print('验证组--RF11模型预测结果')
rf11, rf11_tptnfpfn = evaluation('data/Test_RF_Prob_Predicted.txt', -2, 2, False)
# print("\n")
# print('验证组--TMB预测结果')
tmb, tmb_tptnfpfn = evaluation('data/Test_RF_Prob_Predicted.txt', -1, 2, False)

'''
rf16.insert(5, 0)
rf16.insert(11, 0)
rf16.insert(17, 0)
rf11.insert(5, 0)
rf11.insert(11, 0)
rf11.insert(17, 0)
tmb.insert(5, 0)
tmb.insert(11, 0)
tmb.insert(17, 0)

categories = ["Sensitivity", "Specificity", "Accuracy", "PPV", "NPV", ""]
categories = np.tile(categories, 4)[:-1]  # 重复4次，去除最后一个空占位元素("")
bar_width = 1.1  # 条形宽度
distance = 4  # 每组条形图的间距
# 计算每个柱子的位置
bar_positions_rf16 = np.arange(0, len(categories)*distance, distance)
bar_positions_rf11 = bar_positions_rf16 + bar_width
bar_positions_tmb = bar_positions_rf11 + bar_width
# 调整画布大小
fig = plt.figure(figsize = (16, 4))
# 绘制分组条形图
plt.bar(bar_positions_rf16, rf16, width = bar_width, label = 'RF16', color = "#CF1E36", edgecolor = 'black')
plt.bar(bar_positions_rf11, rf11, width = bar_width, label = 'RF11', color = "#04B83B", edgecolor = 'black')
plt.bar(bar_positions_tmb, tmb, width = bar_width, label = 'TMB', color = "#013E7F", edgecolor = 'black')
plt.legend(
    bbox_to_anchor=(1.0, 0.74),  # 图例位置
    framealpha = 0,  # 隐藏边框
    handlelength = 0.7,  # 图例大小
    fontsize = 14
)  # 添加图例
plt.xlabel("Model evaluation metrics in test set", fontsize = 14)  # x轴标签
plt.ylabel("Value (%)", fontsize = 14)  # y轴标签
plt.ylim(0, 100)  # 指定y轴范围
x_start = bar_positions_rf16[0] - (bar_positions_rf16[6] - bar_positions_tmb[4])/2  # x轴起点
x_end = bar_positions_tmb[len(bar_positions_tmb)-1] + (bar_positions_rf16[6] - bar_positions_tmb[4])/2  # x轴终点
plt.xlim(x_start, x_end)  # 指定x轴范围
plt.yticks(np.arange(0, 101, step = 25))  # 修改y轴刻度
plt.xticks(bar_positions_rf11 + bar_width, categories, rotation = 45, ha = "right", fontsize = 12)  # 设置x轴刻度标签
plt.subplots_adjust(bottom = 0.3)  # 调整图边距，使图完整显示
plt.tick_params(bottom = False)  # 隐藏x轴刻度线
# 去除图右侧和上侧的边框
ax = plt.gca()  # 得到当前轴
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
# 给每组图添加标题（癌症类型）
plt.text(x = bar_positions_rf11[2], y = 105, s = "Pan-cancer", ha = "center", fontsize = 14)
plt.text(x = bar_positions_rf11[8], y = 105, s = "Melanoma", ha = "center", fontsize = 14)
plt.text(x = bar_positions_rf11[14], y = 105, s = "NSCLC", ha = "center", fontsize = 14)
plt.text(x = bar_positions_rf11[20], y = 105, s = "Others", ha = "center", fontsize = 14)
# 添加3条分隔线
plt.plot([bar_positions_rf11[5], bar_positions_rf11[5]], [0, 100], color = "black")
plt.plot([bar_positions_rf11[11], bar_positions_rf11[11]], [0, 100], color = "black")
plt.plot([bar_positions_rf11[17], bar_positions_rf11[17]], [0, 100], color = "black")
# 添加水平虚线
plt.plot([x_start, x_end], [50, 50], "k--", linewidth = 1)
# 保存图片
plt.savefig("plot/evaluation_barplot.pdf", format = "pdf")
# plt.show()
'''
