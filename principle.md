<a id="mulu">目录</a>
<a href="#mulu" class="back">回到目录</a>
<style>
    .back{width:40px;height:40px;display:inline-block;line-height:20px;font-size:20px;background-color:lightyellow;position: fixed;bottom:50px;right:50px;z-index:999;border:2px solid pink;opacity:0.3;transition:all 0.3s;color:green;}
    .back:hover{color:red;opacity:1}
    img{vertical-align:bottom;}
</style>

<!-- @import "[TOC]" {cmd="toc" depthFrom=3 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [数据说明](#数据说明)
    - [一些概念](#一些概念)
    - [源数据各列含义](#源数据各列含义)
- [算法分析](#算法分析)
    - [Model description](#model-description)
    - [Logistic regression analysis](#logistic-regression-analysis)
    - [ROC and precision-recall curve analyses](#roc-and-precision-recall-curve-analyses)
    - [Statistical analyses](#statistical-analyses)

<!-- /code_chunk_output -->

<!-- 打开侧边预览：f1->Markdown Preview Enhanced: open...
只有打开侧边预览时保存才自动更新目录 -->

**文章的主要目的**：开发一个机器学习模型，根据各种因素（或者说指标）预测患者是否对ICB治疗有反应（注意不是预测生存时间或者说预后）
### 数据说明
##### 一些概念
**ICB(immune checkpoint blockade)**：免疫检查点阻断
**TMB**：肿瘤突变负荷，指每百万碱基检测出的体细胞变异总数。在多数肿瘤细胞中，TMB越高，产生的新抗原越多，肿瘤免疫原性越高，越容易被免疫细胞识别，从PD-1/PD-L1免疫检查点抑制剂治疗中的获益越显著
**MSI**：微卫星不稳定性，指肿瘤中某个微卫星位点由于重复单元的插入或缺失而出现新的微卫星等位基因的现象。也常用于预测肿瘤预后，绝大多数MSI不稳定性高的患者，TMB都高；但TMB高的，MSI不稳定性不一定高
**生存相关**：
- 总生存时间`os`：从记录开始至（因任何原因）死亡的时间
- 无进展生存期`PFS`：从记录开始到肿瘤发生（任何方面）进展或（因任何原因）死亡的时间。增加了“发生恶化”这一节点，而“发生恶化”往往早于死亡，所以PFS常常短于OS，因而随访时间短一些。PFS的改善包括了“未恶化”和“未死亡”，即间接和直接地反映了临床获益，它取决于新治疗与现治疗的疗效/风险

**逻辑回归模型**(logistic regression model)：根据给定的自变量数据集来估计事件的发生概率，要求因变量是一个二分类变量（即只能取两个值的变量，比如这篇论文中就是“对ICB治疗有/无反应”），结果是事件发生的概率，这篇论文中就是“对ICB治疗有反应的概率”
**样本统计指标总结**：
- 真阳性(TP): 模型正确地将正样本预测为正类
- 真阴性(TN): 模型正确地将负样本预测为负类
- 假阳性(FP): 模型错误地将负样本预测为正类
- 假阴性(FN): 模型错误地将正样本预测为负类
- 灵敏度(Sensitivity)/召回率(Recall)/真正率(TPR)：在所有实际为正类的样本中，被预测为正类的比例--`TP/(TP+FN)`
- 特异性(Specificity):在所有实际为负类的样本中，被预测为负类的比例--`TN/(TN+FP)`
- 准确率(Accuracy): 所有样本中被正确分类的比例--`(TP+TN)/(TP+TN+FP+FN)`
- 精确率(Precision)/阳性预测值(PPV): 在所有被预测为正类的样本中，实际为正类的比例--`TP/(TP+FP)`
- 阴性预测值(NPV): 在所有被预测为负类的样本中，实际为负类的比例--`TN/(TN+FN)`
- 假正率(FPR)：在所有实际为负类的样本中，被预测为正类的比例--`1-特异性`=`FP/(FP+TN)`

**ROC曲线**：横轴为FPR（假正率），指所有负类样本中，被错误预测为正类的比例；纵轴为TPR（真正率），指所有正类样本中，被正确预测为正类的比例。理想情况下，TPR=1，FPR=0，即图的`(0,1)`点，所以ROC曲线越靠左上角，预测效果越好
- **AUC(Area Under Curve)**；ROC曲线下的面积，值越大则预测效果越好
  - AUC值接近1：模型预测准确率高
  - AUC值略大于0.5：模型预测准确率一般
  - AUC值等于0.5：相当于没有预测效果
  - AUC值小于0.5：相当于反向预测，一般情况下不会出现
- **最优阈值(optimal threshold)**：前面说过，对于二分类模型，模型对于每个样本会给出一个概率值。现需要寻找一个阈值，当概率值超过这个阈值时，说明模型将该样本预测为正类，反之为负类。当预测效果最好（TPR和FPR差值最大）时，这个阈值就称为最优阈值  [具体实现过程](https://blog.csdn.net/uncle_ll/article/details/117255345)

**PRC曲线**：先看平滑不平滑（越平滑越好），再看谁上谁下（同一测试集、一般情况下，上面的比下面的好）
[更多关于这两种曲线](https://blog.csdn.net/pipisorry/article/details/51788927)
![两种曲线](./md-image/两种曲线.png){:width=200 height=200}
如图，红线>绿线>蓝线
**泛癌(pan-cancer)分析**：针对某一个特征横向比较多个癌型，看其敏感性和特异性。其实就是把所有种类（或者说多个种类）的癌症都纳入分析范围

**Brier score**：预测概率与实际结果之间的均方差，取值为0-1，值越小模型预测效果越好
**一致性指数C-index**：类似于AUC，也是用来评价模型的预测能力。通常取值0.5-1，值越大预测效果越好
- 0.5-0.7：较低准确度
- 0.71-0.9：中等准确度
- >0.9：高准确度

计算方法：把所有研究对象随机每2个划为一组。例如在生存分析中，对于一组患者，如果生存时间较长的那个人的预测生存时间也较长，则称之为预测结果与实际结果一致
**风险比(HR)**：用于评估一个二分类因素对生存状态的影响。越远离1，影响越大。比如评估“性别”对患者死亡概率的影响，计算`女性`对`男性`的风险比
- HR=1：男性女性死亡速度相同，性别无影响
- HR>1：女性风险更高，值越大，风险越大。例如HR=2，就是女性死亡速度是男性的2倍
- HR<1：女性风险更低，值越小，风险越小。例如HR=0.5，就是女性死亡速度是男性的一半

**95%置信区间(CI)**：用同样的步骤，去计算置信区间，那么如果重复独立地计算100次，有95%的概率计算出来的区间会包含真实参数值，即大概会有95个置信区间会包含真值。虽然它不是指“CI有95%的概率包括真实参数”，但可以认为真实参数大概率就在CI内，因此通常把CI作为目标参数可能取值的上下界
**混淆矩阵**：展示模型对各类样本的预测情况。混淆矩阵的第`i`行第`j`列为实际为`i`类的样本被预测为`j`类的比例。例如
![混淆矩阵](./md-image/混淆矩阵.png){:width=200 height=200}
已知横坐标是预测值，纵坐标是实际值，左下角的块就表示预测是`NR`但实际为`R`的样本数量和比例。可以看出，`(NR, NR)`和`(R, R)`这两个块的值应越大越好->如果值越大颜色越深，那么就是左上-右下对角线上的块颜色越深，模型预测效果越好

##### 源数据各列含义
| 列名                                                 | 含义                                | 补充                                    |
| ---------------------------------------------------- | ----------------------------------- | --------------------------------------- |
| SAMPLE_ID                                            | 样本编号                            |                                         |
| Cancer_type_grouped_2<br>Cancer_Type2<br>Cancer_Type | 癌症类型                            |                                         |
| Chemo_before_IO                                      | 患者在免疫治疗前是否接受化疗        | 1接受<br>0没接受                        |
| Age                                                  | 年龄                                |                                         |
| Sex                                                  | 性别                                | 1男性<br>0女性                          |
| BMI                                                  | 体重指数                            |                                         |
| Stage                                                | 肿瘤分期                            | 1表示IV期<br>0表示I-III期               |
| Stage at IO start                                    | 患者在免疫治疗前的肿瘤分期          |                                         |
| NLR                                                  | 血液中性粒细胞与淋巴细胞比值        |                                         |
| Platelets                                            | 血小板水平                          |                                         |
| HGB                                                  | 血红蛋白水平                        |                                         |
| Albumin                                              | 白蛋白水平                          |                                         |
| Drug                                                 | 使用的免疫治疗药物                  | 0使用PD1/PDL1或CTLA4<br>1同时使用这两种 |
| Drug_class                                           | 使用的免疫治疗药物名称              |                                         |
| TMB                                                  | 肿瘤突变负荷                        |                                         |
| FCNA                                                 | 拷贝数改变分数                      |                                         |
| HED                                                  | HLA-I的进化差异                     |                                         |
| HLA_LOH                                              | HLA-I杂合性缺失状态                 |                                         |
| MSI                                                  | 微卫星不稳定性                      | 1不稳定<br>0稳定/不确定                 |
| MSI_SCORE                                            | 微卫星不稳定性得分                  |                                         |
| Response                                             | 是否有应答                          | 1应答者<br>0非应答者                    |
| OS_Event                                             | 是否死亡                            | 1死亡<br>0存活                          |
| OS_Months                                            | 总生存时间                          | 以月为单位                              |
| PFS_Event                                            | 是否死亡/肿瘤是否发生恶化           | 1发生<br>0没发生                        |
| PFS_Months                                           | 无进展生存期                        | 以月为单位                              |
| RF16_prob<br>RF11_prob                               | 不属于源数据，是通过sklearn得到的值 |                                         |

`Response`补充说明：将接受了PD-1/PD-L1抑制剂、CTLA-4阻断剂或两种免疫疗法的联合治疗的患者分为不同组
- 出现完全应答complete response(CR)或部分应答partial response(PR)的患者——**应答者responders(R)**
- 疾病无变化stable disease(SD)或发生进展progressive disease(PD)的患者——**非应答者non-responders(NR)**

### 算法分析
在[方法](https://www.nature.com/articles/s41587-021-01070-8#Sec2)一栏中，其中`Patient data description`、`Response, OS and PFS`、`Genomic, demographic, molecular and clinical data`都是在说源数据是怎么来的，以及数据的划分、处理方法、具体含义等等
##### Model description

##### Logistic regression analysis

##### ROC and precision-recall curve analyses

##### Statistical analyses
