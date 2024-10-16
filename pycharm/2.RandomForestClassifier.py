import csv
import pandas as pd
import matplotlib.pyplot as plt
import eli5
from sklearn.ensemble import RandomForestClassifier
from eli5.sklearn import PermutationImportance

data_train = pd.read_excel('41587_2021_1070_MOESM3_ESM.xlsx', sheet_name='Training')
data_test = pd.read_excel('41587_2021_1070_MOESM3_ESM.xlsx', sheet_name='Test')
y_train = data_train[["Response (1:Responder; 0:Non-responder)"]]
y_train.columns = ["Response"]
y_test = data_test[["Response (1:Responder; 0:Non-responder)"]]
y_test.columns = ["Response"]

### RF16
rf16=['Cancer_Type2', 'Albumin', 'HED', 'TMB', 'FCNA', 'BMI', 'NLR', 'Platelets', 'HGB','Stage', 'Age', 'Drug', 'Chemo_before_IO', 'HLA_LOH', 'MSI','Sex']
x_train_col = ["Cancer_Type2", "Albumin", "HED", "TMB", "FCNA", "BMI", "NLR", "Platelets", "HGB", "Stage (1:IV; 0:I-III)", "Age", "Drug (1:Combo; 0:PD1/PDL1orCTLA4)", "Chemo_before_IO (1:Yes; 0:No)", "HLA_LOH", "MSI (1:Unstable; 0:Stable_Indeterminate)", "Sex (1:Male; 0:Female)"]
x_train16 = data_train[x_train_col]
x_test16 = data_test[x_train_col]
x_train16.columns = rf16
x_test16.columns = rf16

## Run random forest classifier
forest16 = RandomForestClassifier(min_samples_split=2, n_estimators=1000, max_depth=8, min_samples_leaf=20, random_state = 0, n_jobs = -1)
forest16.fit(x_train16, y_train.values.ravel())
forest16_predict = forest16.predict(x_test16)

### RF11
rf11=['Stage', 'Drug', 'HED', 'TMB', 'FCNA', 'BMI', 'NLR','HLA_LOH', 'MSI', 'Sex', 'Age']
x_train_col = ["Stage (1:IV; 0:I-III)", "Drug (1:Combo; 0:PD1/PDL1orCTLA4)", "HED", "TMB", "FCNA", "BMI", "NLR", "HLA_LOH", "MSI (1:Unstable; 0:Stable_Indeterminate)", "Sex (1:Male; 0:Female)", "Age"]
x_train11 = data_train[x_train_col]
x_test11 = data_test[x_train_col]
x_train11.columns = rf11
x_test11.columns = rf11

## Run random forest classifier
forest11 = RandomForestClassifier(min_samples_split=2, n_estimators=300, max_depth=4, min_samples_leaf=12, random_state = 0, n_jobs = -1)
forest11.fit(x_train11, y_train.values.ravel())
forest11_predict = forest11.predict(x_test11)

## Save response probability of each sample
header=['Sample_ID', 'Cancer_Type', 'Response', 'OS_Event', 'OS_Months', 'PFS_Event', 'PFS_Months', 'TMB', 'RF16_prob', 'RF11_prob']
data_train.rename(columns = {'Response (1:Responder; 0:Non-responder)': 'Response'}, inplace = True)
data_test.rename(columns = {'Response (1:Responder; 0:Non-responder)': 'Response'}, inplace = True)
with open('Training_RF_Prob.txt', 'w', newline='') as wf:
    wf.write('\t'.join(header) + '\n')
    writer = csv.writer(wf, delimiter='\t')
    writer.writerows(zip(data_train['SAMPLE_ID'], data_train['Cancer_Type2'], data_train['Response'], data_train['OS_Event'], data_train['OS_Months'], data_train['PFS_Event'], data_train['PFS_Months'], data_train['TMB'], forest16.predict_proba(x_train16)[:,1], forest11.predict_proba(x_train11)[:,1]))
with open('Test_RF_Prob.txt', 'w', newline='') as wf:
    wf.write('\t'.join(header) + '\n')
    writer = csv.writer(wf, delimiter='\t')
    writer.writerows(zip(data_test['SAMPLE_ID'], data_test['Cancer_Type2'], data_test['Response'], data_test['OS_Event'], data_test['OS_Months'], data_test['PFS_Event'], data_test['PFS_Months'], data_test['TMB'], forest16.predict_proba(x_test16)[:,1], forest11.predict_proba(x_test11)[:,1]))

## Feature importance of RF16 & RF11
print('\n<RF16_feature Importance>')
perm = PermutationImportance(forest16, scoring = "roc_auc", cv='prefit', random_state = 42).fit(x_train16, y_train)
eli5.show_weights(perm, top = 16, feature_names = x_train16.columns.tolist())

print('\n<RF11_feature Importance>')
perm = PermutationImportance(forest11, scoring = "roc_auc", cv='prefit', random_state = 42).fit(x_train11, y_train)
eli5.show_weights(perm, top = 11, feature_names = x_train11.columns.tolist())

