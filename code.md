<a id="mulu">目录</a>
<a href="#mulu" class="back">回到目录</a>
<style>
    .back{width:40px;height:40px;display:inline-block;line-height:20px;font-size:20px;background-color:lightyellow;position: fixed;bottom:50px;right:50px;z-index:999;border:2px solid pink;opacity:0.3;transition:all 0.3s;color:green;}
    .back:hover{color:red;opacity:1}
    img{vertical-align:bottom;}
</style>

<!-- @import "[TOC]" {cmd="toc" depthFrom=3 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [GridSearch/RandomForestClassifier](#gridsearchrandomforestclassifier)
- [ROC_PRC](#roc_prc)
- [Evaluate_Performance](#evaluate_performance)
- [Brier_score](#brier_score)
- [C-index](#c-index)
- [Survival](#survival)

<!-- /code_chunk_output -->

<!-- 打开侧边预览：f1->Markdown Preview Enhanced: open...
只有打开侧边预览时保存才自动更新目录 -->

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
最后得到两个txt文件(`Test_RF_Prob.txt`和`Training_RF_Prob.txt`)，其中的`RF16_prob`和`RF11_prob`列，分别是验证组和训练组中的样本 使用两个模型(RF16/RF11) 预测的得分（对ICB免疫疗法有反应的概率）
![模型预测打分](./md-image/模型预测打分.png){:width=200 height=200}

---

作者在这部分画了两组图：
- 统计各类癌症NR和R的人数
  ![各种癌症中NR和R的数量](./md-image/各种癌症中NR和R的数量.png){:width=400 height=400}
- 统计RF16模型中各因素的影响大小
  ![feature_bar](./md-image/feature_bar.png){:width=400 height=400}
### ROC_PRC
对于训练组数据，作者根据样本的癌症种类，对上面得到的数据又进行了4次“分组”，分别是
- `Pan-cancer`--包含全部癌症种类（泛癌）
- `NSCLC`--只包含非小细胞肺癌
- `Melanoma`--只包含黑色素瘤
- `Others`--其它

根据这四组数据，作者建了4个`RF16`模型，分别是泛癌模型和3个癌症特异性模型（即每种癌症建一个模型）。
注意：这里所说的“泛癌模型”和“癌症特异性模型”，都是基于上面的`RF16_prob`和`RF11_prob`打分，只是选取的最佳阈值不同（泛癌模型是对全部样本计算，而癌症特异性模型是将不同癌症的样本分开来计算）
对每个模型都画了ROC和PRC曲线，并计算了各自的最佳阈值，结果保存在`Pan_Thresholds.txt`（泛癌模型）和`Thresholds.txt`（癌症特异性模型）中
以“训练组--泛癌”为例：
- **ROC-PRC曲线及其具体数值**：
  ![ROCPRC1](./md-image/ROCPRC1.png){:width=250 height=250}
  ![ROCPRC2](./md-image/ROCPRC2.png){:width=300 height=300}
  可以看到RF16模型在ROC中最靠左上角，在PRC中最平滑且靠上，对患者是否有应答的预测能力最好
- **在ROC曲线上取最佳阈值**：
  ![最佳阈值1](./md-image/最佳阈值1.png){:width=400 height=400}
  ![最佳阈值2](./md-image/最佳阈值2.png){:width=80 height=80}
  曲线上标的那个点就是最佳阈值点，点上标注的是`最佳阈值 (特异度, 敏感度)`

**所有的最佳阈值结果**：
![最佳阈值](./md-image/最佳阈值.png){:width=400 height=400}
对于验证组，分组方式同训练组，但只画了ROC和PRC曲线，没有计算最佳阈值；在后面的计算中，验证组只使用癌症特异性模型，使用的最佳阈值是`Thresholds.txt`（因为都是癌症特异性模型）

---

作者在这部分画了两组图：
- 各模型（`RF16`/`RF11`/`TMB`）对泛癌和3种癌症的**ROC曲线**：
  - 验证组：
    ![ROC曲线](./md-image/ROC曲线.png){:width=250 height=250}
  - 测试组：
    ![ROC曲线2](./md-image/ROC曲线2.png){:width=250 height=250} 
  
  可以看到验证组和测试组中，`RF16`模型对各种癌症预测的AUC均最高
- **小提琴图**：将数据按NR和R、癌症种类的不同进行分组，分别比较RF16预测结果和TMB
  - `RF16_prob`--癌症种类：
  ![violin_plot1](./md-image/violin_plot1.png){:width=400 height=400}
  - log~2~(TMB+1)--癌症种类：
  ![violin_plot2](./md-image/violin_plot2.png){:width=400 height=400}

可以看到，在4种癌症中，RF16模型预测得分的组间差异都明显大于TMB的
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

---

作者在这部分画了两组图：
- **混淆矩阵**：展示验证组中，`RF16`和`TMB`模型对各种癌症的预测结果（TP、TN、FP、FN）。这里以这两个模型对泛癌的预测结果为例：
  ![evaluation_matrix](./md-image/evaluation_matrix.png){:width=300 height=300}
- **柱状图**：展示验证组中，各模型对各种癌症的预测结果（灵敏度、特异性、准确率、阳/阴性预测值）
  ![evaluation_barplot](./md-image/evaluation_barplot.png){:width=250 height=250}
  横坐标就是5种预测结果，纵坐标是结果值（以百分比为单位），不同颜色代表不同模型，共分成了4大组（每组间以竖线分隔）

---

文章最前面概述部分也画了一个混淆矩阵，可能使用的是测试组泛癌的预测结果
![matrix_all](./md-image/matrix_all.png){:width=300 height=300}
### Brier_score
进行生存分析，探究模型预测得分（`RF16_prob`/`RF11_prob`/`TMB`）与生存状态`OS`的关系
也是将训练组和验证组分开来，每组都进行泛癌、Melanoma、NSCLC、Others共4组分析，计算了Brier score并绘制了Prediction error curves图
以“训练组--Pan-cancer”为例：
- **Brier score分析结果**：
  ![Brier_score1](./md-image/Brier_score1.png){:width=400 height=400}
  红框内的就是各模型关于生存状态的总Brier score
  - `Reference`：画图函数提供的，使用`marginal  Kaplan-Meier`方法建模进行预测的结果
- **Prediction error curves图**：
  ![Brier_score2](./md-image/Brier_score2.png){:width=400 height=400}
  该图展示了模型对不同生存时间的患者的预测能力，纵坐标`是Brier score`，因此曲线越靠下预测效果越好。可以看到RF16（红色线）对生存状态的预测能力几乎也是最好的
### C-index
计算了训练组和验证组中，`RF16_prob`/`RF11_prob`/`TMB`这3个模型对于两种生存状态（`OS`和`PFS`）的预测能力，也是分成泛癌、Melanoma、NSCLC、Others共4组，并比较了每个模型c-index值的差异
以测试组--Melanoma--OS为例：
![cindex1](./md-image/cindex1.png){:width=120 height=120}
![cindex2](./md-image/cindex2.png){:width=400 height=400}
可以看到`RF16`的cindex值较高，且与另两组间p值基本都<0.05，说明`RF16`显著优于另两组模型
### Survival
进行生存分析：根据`RF16`模型的预测结果，将样本分为`R`和`NR`两组，计算这两组生存状态的差异
以测试组--Melanoma--OS为例：
![Survival2](./md-image/Survival2.png){:width=250 height=250}
绘制survplot图：
![Survival1](./md-image/Survival1.png){:width=400 height=400}
横坐标是时间，下面图的纵坐标是存活人数，即在两组中，在对应时间有多少人还存活；上面图的纵坐标是生存概率，根据下面图的存活人数/总人数计算得到
可以看到`R`（有应答）组的生存概率明显高于`NR`（无应答）组，HR值为0.24（远小于1），p值<0.05且CI没有跨过“1”这个点（说明得到的HR有统计学意义），说明模型的分组能较准确地预测生存状态

---

在作者提供的代码中，对于训练组和验证组这2组，作者用`RF16`/`TMB`这2个模型都画了图，每组都分为泛癌+3种癌症共4种，生存状态也分为`OS`和`PFS`2种，因此共画了2\*3\*4\*2=32张图，但论文实际呈现的图只有验证组的`RF16`模型的8张图，因此我的代码中也只画了这8张（[C-index](#c-index)也是）
作者将cindex和生存分析的结果画到了一张图中，还是以测试组--Melanoma--OS为例：
![Survival3](./md-image/Survival3.png){:width=400 height=400}
