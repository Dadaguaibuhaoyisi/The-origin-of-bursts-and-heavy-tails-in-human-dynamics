import pandas as pd
import matplotlib.pyplot as plt#约定俗成的写法plt
import numpy as np
from tqdm import tqdm
import datetime
import seaborn as sns
sns.set(font='SimSun',font_scale=1.5, palette="muted", color_codes=True, style = 'white')#字体  Times New Roman   SimHei
#解决中文显示问题
plt.rcParams['font.sans-serif']=['SimSun']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'cm'
# %matplotlib inline
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['font.family'] = 'SimSun'#'Times New Roman'

def get_dict(t_max,task_length,p_high):
    # 初始设置（等待时长最小是1）
    t_dict = {}
    task_name_list = [i for i in range(task_length)]
    priority_list = list(np.random.random(size=task_length)) # random ：Uniformly distributed floats over ``[0, 1)``
    for i in range(task_length):
        t_dict[task_name_list[i]] = 1#0
    task_name_set = set(range(task_length))
    for t in tqdm(range(1,t_max+1)):
        # p的概率按最高优先级的来，1-p的概率随机选择
        # 1:找出最高的
        index_highest = priority_list.index(max(priority_list))
        print(index_highest, priority_list[index_highest])
        # 2:随机选择一个
        index_random = np.random.randint(task_length)
        print(index_random, priority_list[index_random])
        # 二者之间按概率选一个
        p_rand = 1 - p_high
        index_execute = np.random.choice([index_highest,index_random],1,p=[p_high, p_rand])[0]
        # 更新任务列表，优先级列表，任务名称库
        del task_name_list[index_execute]
        del priority_list[index_execute]
        task_name_list.append(max(task_name_set)+1)
        task_name_set = task_name_set | set(task_name_list)
        priority_list.append(np.random.random())
        print(len(task_name_list),len(priority_list),len(task_name_set))
        # 更新等待时长字典
        for i in range(task_length):
            try:
                t_dict[task_name_list[i]] += 1
            except:
                t_dict[task_name_list[i]] = 1#0
#         print('经过%i次任务执行之后'%t,'，每个任务的等待时长：\n',t_dict)
        print(len(t_dict))
        print('*'*80)
    return t_dict

# 最小等待时间 = 1
t_max = 1000000
task_length = 100
p_high = 0.99999#或者0.00001
t_dict = get_dict(t_max,task_length,p_high)
df = pd.DataFrame(t_dict, index = [0])
df.to_csv('%f.csv'%p_high, index = None)


import powerlaw
data = list(t_dict.values())
fit = powerlaw.Fit(data, discrete=True)
print('xmin\t=',fit.xmin )
print ('alpha\t=',fit.power_law.alpha)
print ('sigma\t=',fit.power_law.sigma)
print ('D\t=',fit.power_law.D)
print(fit.distribution_compare('power_law', 'exponential'))#If greater than 0, the first distribution is preferred.
plt.title('p=%f'%p_high)
plt.xlabel('等待时间')
plt.ylabel('概率')
fig = fit.plot_pdf(linewidth = 4, label='真实等待时间概率分布')
fit.power_law.plot_pdf(ax=fig, color='red', linestyle='--', label='Power law拟合')
fit.exponential.plot_pdf(ax=fig, color='blue', linestyle='--', label='Exponential拟合')
plt.legend()
plt.savefig('%f.jpg'%p_high,dpi=300)
plt.savefig('%f.pdf'%p_high,dpi=300)
