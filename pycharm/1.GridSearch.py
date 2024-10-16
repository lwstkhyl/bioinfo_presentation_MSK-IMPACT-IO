import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

data = pd.read_excel('41587_2021_1070_MOESM3_ESM.xlsx', sheet_name='Training')
x_train_col = ["Cancer_Type2", "Albumin", "HED", "TMB", "FCNA", "BMI", "NLR", "Platelets", "HGB", "Stage (1:IV; 0:I-III)", "Age", "Drug (1:Combo; 0:PD1/PDL1orCTLA4)", "Chemo_before_IO (1:Yes; 0:No)", "HLA_LOH", "MSI (1:Unstable; 0:Stable_Indeterminate)", "Sex (1:Male; 0:Female)"]
x_train = data[x_train_col]
rf16 = ["Cancer_Type2", "Albumin", "HED", "TMB", "FCNA", "BMI", "NLR", "Platelets", "HGB", "Stage", "Age", "Drug", "Chemo_before_IO", "HLA_LOH", "MSI", "Sex"]
x_train.columns = rf16
y_train = data[["Response (1:Responder; 0:Non-responder)"]]
y_train.columns = ["Response"]

params = { 'n_estimators' : list(range(100, 1100, 100)),
           'max_depth' : list(range(2, 22, 2)),
           'min_samples_leaf' : list(range(2, 22, 2)),
           'min_samples_split' : list(range(2, 22, 2))
            }

# 注：运行时间可能长达数小时，取决于CPU性能
# 我的运行时间：RF16--约2h RF11--约1h45min
# ## GridSearchCV for RF16
rf_clf = RandomForestClassifier(random_state = 0, n_jobs = -1)
grid_cv = GridSearchCV(rf_clf, param_grid = params, cv = 5, n_jobs = -1)
# 打印进度：加上verbose = 1参数
# grid_cv = GridSearchCV(rf_clf, param_grid = params, cv = 5, n_jobs = -1, verbose = 1)
grid_cv.fit(x_train, y_train.values.ravel())

print('Optimal Hyper Parameter, RF16: ', grid_cv.best_params_)
print('Maximum Accuracy, RF16: {:.4f}'.format(grid_cv.best_score_))

## GridSearchCV for RF11
rf11=["HED", "TMB", "FCNA", "BMI", "NLR", "Stage", "Age", "Drug", "HLA_LOH", "MSI", "Sex"]
x_train_col = ["HED", "TMB", "FCNA", "BMI", "NLR", "Stage (1:IV; 0:I-III)", "Age", "Drug (1:Combo; 0:PD1/PDL1orCTLA4)", "HLA_LOH", "MSI (1:Unstable; 0:Stable_Indeterminate)", "Sex (1:Male; 0:Female)"]
x_train = data[x_train_col]
x_train.columns = rf11
rf_clf = RandomForestClassifier(random_state = 0, n_jobs = -1)
grid_cv = GridSearchCV(rf_clf, param_grid = params, cv = 5, n_jobs = -1)
# grid_cv = GridSearchCV(rf_clf, param_grid = params, cv = 5, n_jobs = -1, verbose = 1)
grid_cv.fit(x_train, y_train.values.ravel())

print('Optimal Hyper Parameter, RF11: ', grid_cv.best_params_)
print('Maximum Accuracy, RF11: {:.4f}'.format(grid_cv.best_score_))
