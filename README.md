# The-origin-of-bursts-and-heavy-tails-in-human-dynamics
复现The origin of bursts and heavy tails in human dynamics的实验过程，看是否出现等待时间的幂律分布。


可以改变的参数：
1. 任务列表长度：task_length(本实验设置为100）
2. 选择最高优先级任务进行执行的概率：p_high（本实验设置为0.99999和0.00001）
3. 实验演化次数：t_max（本实验设置为10^6）


结果：
1. 当p_high=0.99999时→相当于纯按最高优先级的先执行
2. 当p_high=0.00001时→相当于随机选择任务执行
实验结果见文档“实验结果记录.docx”，不知道什么原因造成了我的s实验结果在当p_high=0.99999时幂律分布指数不是-1，而是-6。
