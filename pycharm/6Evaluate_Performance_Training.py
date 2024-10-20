## Evaluate model performance using cancer-type-specific thresholds

def isfloat(n):
    try:
        float(n)
    except:
        return False
    return True


rf = open('../r/data/Thresholds.txt', 'r')
line = rf.readline()
cutoff = []
while line != '':
    line = line.split()
    if isfloat(line[0]):
        cutoff.append(round(float(line[0]), 3))
    line = rf.readline()
rf.close()

# 根据癌症种类，建了3个模型，有3个最佳阈值。用某个种类癌症建的模型去预测该种类癌症的样本是R还是NR
# 在data/Training_RF_Prob.txt中新添两列，一列是RF16模型预测结果，另一列是TMB是否≥10，如果是则为R，否则为NR
rf = open('data/Training_RF_Prob.txt', 'r')
wf = open('Training_RF_Prob_Predicted_new.txt', 'w')  # 结果写入到这个文件
line = rf.readline()
while line != '':
    line = line.strip().split('\t')
    if line[0] == 'Sample_ID':
        wf.write('\t'.join(line) + '\t' + 'RF16' + '\t' + 'TMB_10' + '\n')
    else:
        cancer_type = int(line[1])
        RF16_res = "R" if float(line[-2]) >= cutoff[cancer_type] else "NR"
        TMB10_res = "R" if float(line[-3]) >= float(10) else "NR"
        wf.write('\t'.join(line) + '\t' + RF16_res + '\t' + TMB10_res + '\n')
    line = rf.readline()
rf.close()
wf.close()


def evaluation(input, target):
    order = ['Melanoma', 'NSCLC', 'Others']
    tp_p = tn_p = fp_p = fn_p = 0
    for i in range(3):
        rf = open(input, 'r')
        line = rf.readline()
        tp = tn = fp = fn = 0
        while line != '':
            line = line.strip().split('\t')
            if line[0] != 'Sample_ID':
                if line[1] == str(i):
                    if line[2] == '1':
                        if line[target] == 'R':
                            tp += 1
                            tp_p += 1
                        else:
                            fn += 1
                            fn_p += 1
                    else:
                        if line[target] == 'R':
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
        print(str(sensitivity) + '\t' + str(specificity) + '\t' + str(accuracy) + '\t' + str(ppv) + '\t' + str(
            npv) + '\n')
        rf.close()
    print('Pan-cancer')
    print(str(tn_p) + '\t' + str(fp_p) + '\n' + str(fn_p) + '\t' + str(tp_p) + '\n')
    sensitivity_p = float(tp_p) / (float(tp_p + fn_p)) * 100
    specificity_p = float(tn_p) / (float(fp_p + tn_p)) * 100
    accuracy_p = float(tp_p + tn_p) / (float(tp_p + fp_p + fn_p + tn_p)) * 100
    ppv_p = float(tp_p) / (float(tp_p + fp_p)) * 100
    npv_p = float(tn_p) / (float(fn_p + tn_p)) * 100
    print(str(sensitivity_p) + '\t' + str(specificity_p) + '\t' + str(accuracy_p) + '\t' + str(ppv_p) + '\t' + str(
        npv_p) + '\n')


print('<Performance evaluation for RF16 using cancer-type-specific thresholds>')
evaluation('data/Training_RF_Prob_Predicted.txt', -2)

print('<Performance evaluation for TMB>')
evaluation('data/Training_RF_Prob_Predicted.txt', -1)

