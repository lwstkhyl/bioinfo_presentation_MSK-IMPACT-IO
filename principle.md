### 数据说明
##### R/NR
将接受了PD-1/PD-L1抑制剂、CTLA-4阻断剂或两种免疫疗法的联合治疗的患者分为不同组：
- 出现完全应答complete response(CR)或部分应答partial response(PR)的患者——**应答者responders(R)**
- 疾病无变化stable disease(SD)或进展progressive disease(PD)的患者——**非应答者non-responders(NR)**
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
| PFS_Event                                            | 是否死亡/肿瘤是否发送恶化           | 1发生<br>0没发生                        |
| PFS_Months                                           | 无进展生存期                        | 以月为单位                              |
| RF16_prob<br>RF11_prob                               | 不属于源数据，是通过sklearn得到的值 |                                         |

补充：总生存`os`和无进展生存期`PFS`
- 总生存：从记录开始至（因任何原因）死亡的时间
- 无进展生存期：从记录开始到肿瘤发生（任何方面）进展或（因任何原因）死亡的时间。增加了“发生恶化”这一节点，而“发生恶化”往往早于死亡，所以PFS常常短于OS，因而随访时间短一些。PFS的改善包括了“未恶化”和“未死亡”，即间接和直接地反映了临床获益，它取决于新治疗与现治疗的疗效/风险



### 算法分析
##### Model description

##### Logistic regression analysis

##### ROC and precision-recall curve analyses

##### Statistical analyses
