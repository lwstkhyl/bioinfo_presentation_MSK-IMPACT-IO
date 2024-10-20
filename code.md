### GridSearch/RandomForestClassifier
这部分主要探究：构造的模型中，哪些因素的影响最大
作者首先按癌症类型将数据集随机分成训练/验证组，训练组有80%的样本(n=1184)、验证组有20%的样本(n=295)
之后作者先选了16个因素，包括癌症类型、Albumin、HED、TMB、FCNA、BMI、NLR、Platelets、HGB、Stage、Age、Drug、Chemo_before_IO、HLA_LOH、MSI、Sex，基于它们使用`GridSearch`方法构建了一个模型`RF16`，之后又用`PermutationImportance`方法评估每个因素对模型的贡献（影响）
![RF16_feature](./md-image/RF16_feature.png){:width=400 height=400}
如图所示，`Weight`就是贡献大小
其中肿瘤突变负荷`TMB`的贡献最大，这与许多其它研究的结果一致；化疗史`Chemo_before_IO`对ICB反应的影响与TMB相似；MSI状态并未被模型选为主要预测因子之一，可能是因为它与TMB密切相关

---

之后作者为了评估将癌症类型、`Chemo_before_IO`以及血液标志物(`Platelets`、`HGB`、`Albumin`)与其他因素相结合的预测能力，又选了11个因素，包括HED、TMB、FCNA、BMI、NLR、Stage、Age、Drug、HLA_LOH、MSI、Sex（注意这里不是上面RF16中影响最大的11个因素），目的是确定以前未广泛使用的其他因素（指影响较小的因素？）来预测ICB
建模方法同上，结果如下
![RF11_feature](./md-image/RF11_feature.png){:width=300 height=300}

---

**两种模型的准确性**：
![GridSearch](./md-image/GridSearchCV.png){:width=150 height=150}
RF16模型的最高准确率为0.7559，RF16模型的最高准确率为0.7576（由于我这里只运行了一次，不一定是最高值）
最后得到两个txt文件(`Test_RF_Prob.txt`和`Training_RF_Prob.txt`)，分别是验证组和训练组中的样本 使用两个模型(RF16/RF11) 预测的得分（对ICB免疫疗法有反应的概率）
![模型预测打分](./md-image/模型预测打分.png){:width=200 height=200}
### ROC_PRC_Training/Test
对于训练组数据，作者根据样本的癌症种类，对上面得到的数据又进行了4次“分组”，分别是
- `Pan-cancer`--包含全部癌症种类（泛癌）
- `NSCLC`--只包含非小细胞肺癌
- `Melanoma`--只包含黑色素瘤
- `Others`--其它

根据这四组数据，作者建了4个`RF16`模型，分别是泛癌模型和3个癌症特异性模型（即每种癌症建一个模型）。
对每个模型都画了ROC和PRC曲线，并计算了模型的最佳阈值，结果保存在`Pan_Thresholds.txt`（泛癌模型）和`Thresholds.txt`（癌症特异性模型）中
![最佳阈值](./md-image/最佳阈值.png){:width=400 height=400}
对于验证组，分组方式同训练组，但只画了ROC和PRC曲线，没有计算最佳阈值；在后面的计算中，验证组只使用癌症特异性模型，使用的最佳阈值是`Thresholds.txt`（因为都是癌症特异性模型）
### Evaluate_Performance
在这一部分（5-7的python代码）中，作者干了2件事
- 在最早的`Test_RF_Prob.txt`和`Training_RF_Prob.txt`中新添一列或两列，标明模型或者TMB预测各样本是R还是NR
  - 如果RF16模型给出的预测值(`RF16_prob`)≥最佳阈值，就说明模型预测该样本为R（应答者），否则为NR（非应答者）
    注：如果是特异性模型，就根据每个样本的癌症种类选择对应的癌症模型阈值。比如这个样本是Melanoma，就找Melanoma模型的最佳阈值，将`RF16_prob`与这个阈值比较
  - 如果TMB≥10，则根据TMB的预测结果为R，否则为NR
  
  训练组的泛癌模型数据只统计了RF16模型预测结果`Training_RF_Prob_Pan_Predicted.txt`，训练组和验证组的癌症特异性模型数据统计了RF16模型和TMB预测结果`Training_RF_Prob_Predicted.txt`/`Test_RF_Prob_Predicted.txt`
  ![Evaluate_Performance1](./md-image/Evaluate_Performance1.png){:width=600 height=600}
- 根据上面的预测结果，计算并输出各模型对各种癌症的预测灵敏度、特异性、准确率、阳/阴性预测值
  其实就是统计上面图中5组预测结果（5个红框），与真实值`Response`相对比，看看预测对了没
  ![Evaluate_Performance2](./md-image/Evaluate_Performance2.png){:width=600 height=600}
  类似的还有4个输出，除了上面的“训练组--泛癌模型预测结果”，还有“训练组--特异性模型预测结果”、“训练组--TMB预测结果”、“验证组--特异性模型预测结果”、“验证组--TMB预测结果”
