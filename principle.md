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

##### R/NR
将接受了PD-1/PD-L1抑制剂、CTLA-4阻断剂或两种免疫疗法的联合治疗的患者分为不同组：
- 出现完全应答complete response(CR)或部分应答partial response(PR)的患者——**应答者responders(R)**
- 疾病无变化stable disease(SD)或发生进展progressive disease(PD)的患者——**非应答者non-responders(NR)**
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

### 算法分析
在[方法](https://www.nature.com/articles/s41587-021-01070-8#Sec2)一栏中，其中`Patient data description`、`Response, OS and PFS`、`Genomic, demographic, molecular and clinical data`都是在说源数据是怎么来的，以及数据的划分、处理方法、具体含义等等
##### Model description

##### Logistic regression analysis

##### ROC and precision-recall curve analyses

##### Statistical analyses
