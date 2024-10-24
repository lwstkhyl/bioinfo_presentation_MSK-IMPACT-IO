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


rf16.insert(4, 0)
rf16.insert(10, 0)
rf16.insert(16, 0)
rf11.insert(4, 0)
rf11.insert(10, 0)
rf11.insert(16, 0)
tmb.insert(4, 0)
tmb.insert(10, 0)
tmb.insert(16, 0)

categories = ["Sensitivity", "Specificity", "Accuracy", "PPV", "NPV", "", "Sensitivity", "Specificity", "Accuracy", "PPV", "NPV", "", "Sensitivity", "Specificity", "Accuracy", "PPV", "NPV", "", "Sensitivity", "Specificity", "Accuracy", "PPV", "NPV"]
bar_width = 0.3  # 条形宽度
bar_positions_rf16 = np.arange(len(categories))
bar_positions_rf11 = bar_positions_rf16 + bar_width
bar_positions_tmb = bar_positions_rf11 + bar_width
# 绘制分组条形图
plt.bar(bar_positions_rf16, rf16, width = bar_width, label = 'RF16')
plt.bar(bar_positions_rf11, rf11, width = bar_width, label = 'RF11')
plt.bar(bar_positions_tmb, tmb, width = bar_width, label = 'TMB')
# 添加图例
plt.legend()
# 设置x轴刻度和标签
plt.xticks(bar_positions_rf11, categories)



plt.show()

