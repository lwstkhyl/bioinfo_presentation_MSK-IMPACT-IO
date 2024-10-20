# 文件中的某行是不是数字
def isfloat(n):
    try:
        float(n)
    except:
        return False
    return True


# 从文件中读取阈值
def get_cutoff(thresholds_file_path):
    rf = open(thresholds_file_path, 'r')
    line = rf.readline()
    cutoff = []  # 是前面得到的最佳阈值
    while line != '':
        line = line.split()
        if isfloat(line[0]):
            cutoff.append(round(float(line[0]), 3))
        line = rf.readline()
    rf.close()
    return cutoff


def write_res(data_path, des_path, thresholds_file_path, have_TMB = False):
    """
    在data_path中新添一列或两列，标明模型或者TMB预测各样本是R还是NR。
    如果RF16模型给出的预测值(RF16_prob)≥阈值，就说明模型预测该样本为R（响应者），否则为NR；
    如果TMB≥10，则预测为R，否则为NR。
    have_TMB为False时，使用泛癌模型（使用全部癌症种类构建的），反之使用癌症特异性模型（根据不同癌症模型预测不同癌症的患者）
    :param data_path: Training_RF_Prob/Test_RF_Prob
    :param des_path: 文件输出路径
    :param thresholds_file_path: Pan_Thresholds/Thresholds
    :param have_TMB: 是否根据TMB预测
    """
    cutoff = get_cutoff(thresholds_file_path)
    rf = open(data_path, 'r')
    wf = open(des_path, 'w')  # 结果写入到这个文件
    line = rf.readline()
    while line != '':
        line = line.strip().split('\t')
        if line[0] == 'Sample_ID':  # 如果是第一行（列名），就直接写入文件中作为列名
            wf.write('\t'.join(line) + '\t' + 'RF16' + (('\t' + 'TMB_10') if have_TMB else "") + '\n')
        else:
            cancer_type = int(line[1]) if have_TMB else 0
            RF16_res = ('\t' + "R") if float(line[-2]) >= cutoff[cancer_type] else ('\t' + "NR")
            TMB10_res = (('\t' + "R") if float(line[-3]) >= float(10) else ('\t' + "NR")) if have_TMB else ""
            wf.write('\t'.join(line) + RF16_res + TMB10_res + '\n')
        line = rf.readline()
    rf.close()
    wf.close()

# # 泛癌模型--训练组
# write_res('Training_RF_Prob.txt', 'Training_RF_Prob_Pan_Predicted.txt', '../r/Pan_Thresholds.txt', False)
# # 癌症特异模型--训练组
# write_res('Training_RF_Prob.txt', 'Training_RF_Prob_Predicted.txt', '../r/Thresholds.txt', True)
# # 癌症特异模型--验证组
# write_res('Test_RF_Prob.txt', 'Test_RF_Prob_Predicted.txt', '../r/Thresholds.txt', True)

print('<Performance evaluation for RF16 using pan-cancer threshold>')
order = ['Melanoma', 'NSCLC', 'Others']
tp_p = tn_p = fp_p = fn_p = 0
for i in range(3):
    rf = open('Training_RF_Prob_Pan_Predicted.txt', 'r')
    line = rf.readline()
    tp = tn = fp = fn = 0
    while line != '':
        line = line.strip().split('\t')
        if line[0] != 'Sample_ID':
            if line[1] == str(i):
                if line[2] == '1':
                    if line[-1] == 'R':
                        tp += 1
                        tp_p += 1
                    else:
                        fn += 1
                        fn_p += 1
                else:
                    if line[-1] == 'R':
                        fp += 1
                        fp_p += 1
                    else:
                        tn += 1
                        tn_p += 1
        line = rf.readline()
    print(order[i])
    print(str(tn) + '\t' + str(fp) + '\n' + str(fn) + '\t' + str(tp) + '\n')
    sensitivity = float(tp) / (float(tp + fn)) * 100
    specificity = float(tn) / (float(fp + tn)) * 100
    accuracy = float(tp + tn) / (float(tp + fp + fn + tn)) * 100
    ppv = float(tp) / (float(tp + fp)) * 100
    npv = float(tn) / (float(fn + tn)) * 100
    print(str(sensitivity) + '\t' + str(specificity) + '\t' + str(accuracy) + '\t' + str(ppv) + '\t' + str(npv) + '\n')
    rf.close()
print('Pan-cancer')
print(str(tn_p) + '\t' + str(fp_p) + '\n' + str(fn_p) + '\t' + str(tp_p) + '\n')
sensitivity_p = float(tp_p) / (float(tp_p + fn_p)) * 100
specificity_p = float(tn_p) / (float(fp_p + tn_p)) * 100
accuracy_p = float(tp_p + tn_p) / (float(tp_p + fp_p + fn_p + tn_p)) * 100
ppv_p = float(tp_p) / (float(tp_p + fp_p)) * 100
npv_p = float(tn_p) / (float(fn_p + tn_p)) * 100
print(str(sensitivity_p) + '\t' + str(specificity_p) + '\t' + str(accuracy_p) + '\t' + str(ppv_p) + '\t' + str(npv_p) + '\n')

