import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 统计各类癌症NR和R的人数（文中有1400+个数据，作者提供的原数据只有不到1200个，所以画出的图不同）
data = pd.read_excel('41587_2021_1070_MOESM3_ESM.xlsx', sheet_name='Training')
sum_num = data["Cancer_type_grouped_2"].value_counts()  # 统计该列每个值出现的次数
sum_num_df = pd.DataFrame({'sum_num': sum_num.values}, index = sum_num.index)
r_num = data.query('`Response (1:Responder; 0:Non-responder)` == 1')["Cancer_type_grouped_2"].value_counts()
r_num_df = pd.DataFrame({'r_num': r_num.values}, index = r_num.index)
nr_num = data.query('`Response (1:Responder; 0:Non-responder)` == 0')["Cancer_type_grouped_2"].value_counts()
nr_num_df = pd.DataFrame({'nr_num': nr_num.values}, index = nr_num.index)
all_num = pd.merge(sum_num_df, r_num_df, left_index=True, right_index=True, how='left')  # 合并，保留sum_num的所有行，允许缺失值
all_num = pd.merge(all_num, nr_num_df, left_index=True, right_index=True, how='left')
all_num.fillna(0, inplace=True)  # 填充NA值
# all_num.to_csv('data/r_nr_num.csv')
# 画图
bar_width = 0.7  # 柱子宽度
font_size = 14  # 字号
bar_distance = 0.2  # 最上面与最下面的柱子与图边框的距离
text_x = 0.05  # 文本在x轴向右的偏移量
text_y = 0.15  # 文本在y轴向下的偏移量
legend_x = 0.85  # 图例x位置
legend_y = 0.25  # 图例x位置
legend_size = 0.7  # 图例大小
label_pad = 10  # xy轴标签与轴的距离
# all_num = pd.read_csv('data/r_nr_num.csv', index_col=0, header=0)
all_num = all_num[::-1]  # 倒转顺序
x = list(all_num.index)  # x轴
fig = plt.figure(figsize=(8, 8))  # 调整画布大小
plt.barh(x, all_num.nr_num, color="#00B0BB", label='Non-responder (NR)', edgecolor='black', height=bar_width)  # 横向柱状图
plt.barh(x, all_num.r_num, left=all_num.nr_num, color="#E7B800", label='Response (R)', edgecolor='black', height=bar_width)  # 进行堆叠
plt.xlim(0, 600)  # 指定x轴范围
plt.ylim(-bar_width/2-(1-bar_width)/2, len(x)-1+bar_width/2+(1-bar_width)/2)  # 指定y轴范围
# 去除图右侧和上侧的边框
ax = plt.gca()  # 得到当前轴
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
# 添加图例
plt.legend(
    bbox_to_anchor=(legend_x, legend_y),  # 图例位置
    framealpha=0,  # 隐藏边框
    handlelength=legend_size,  # 图例大小
    fontsize=font_size
)
plt.tick_params(left=False)  # 隐藏y轴刻度线
plt.xlabel("Number of patients (${n}$)", fontsize=font_size, labelpad=label_pad)  # x轴标签
plt.ylabel("Cancer type", fontsize=font_size, labelpad=label_pad)  # y轴标签
plt.xticks(fontsize=font_size)  # x轴刻度标签
plt.yticks(fontsize=font_size)  # y轴刻度标签
# 添加每个柱子的文字
for i in range(len(x)):
    plt.annotate(
        s=f"({int(all_num.iloc[i, 2])}/{int(all_num.iloc[i, 1])})",
        xy=(all_num.iloc[i, 0]+text_x*100, i-text_y),
        fontsize=font_size
    )
# 保存图片
plt.savefig("plot/nr_r_count_barplot.pdf", format="pdf", bbox_inches='tight', pad_inches=0.5)
# plt.show()


