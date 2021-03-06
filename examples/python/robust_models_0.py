# coding: utf-8

# DO NOT EDIT
# Autogenerated from the notebook robust_models_0.ipynb.
# Edit the notebook and then sync the output with this file.
#
# flake8: noqa
# DO NOT EDIT

# # 稳健线性回归

import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.sandbox.regression.predstd import wls_prediction_std

# ## 估算值
#
# 加载数据:

data = sm.datasets.stackloss.load()
data.exog = sm.add_constant(data.exog)

# Huber 的 T 范数具有（默认）中位数绝对偏差标度

huber_t = sm.RLM(data.endog, data.exog, M=sm.robust.norms.HuberT())
hub_results = huber_t.fit()
print(hub_results.params)
print(hub_results.bse)
print(
    hub_results.summary(
        yname='y',
        xname=['var_%d' % i for i in range(len(hub_results.params))]))

# Huber 的 T 范数 具有关于'H2' 协方差矩阵

hub_results2 = huber_t.fit(cov="H2")
print(hub_results2.params)
print(hub_results2.bse)

# Andrew's Wave 范数具有 Huber 的 Proposal 建议 2 倍缩放比例且关于 'H3' 协方差矩阵

andrew_mod = sm.RLM(data.endog, data.exog, M=sm.robust.norms.AndrewWave())
andrew_results = andrew_mod.fit(
    scale_est=sm.robust.scale.HuberScale(), cov="H3")
print('Parameters: ', andrew_results.params)

# 有关更多的选项，请参见 ``help(sm.RLM.fit)`` ；有关缩放选项，请参见 ``module sm.robust.scale``

#
# ## OLS 与 RLM 的比较
#
# 具有异常值的人工数据:

nsample = 50
x1 = np.linspace(0, 20, nsample)
X = np.column_stack((x1, (x1 - 5)**2))
X = sm.add_constant(X)
sig = 0.3  # 较小的误差方差可使 OLS<->RLM 之间的对比度更大
beta = [5, 0.5, -0.0]
y_true2 = np.dot(X, beta)
y2 = y_true2 + sig * 1. * np.random.normal(size=nsample)
y2[[39, 41, 43, 45, 48]] -= 5  # 添加一些异常值 (以 10% 的 nsample 抽样比例)

# ### 示例1: 具有线性真值的二次函数
#
# 请注意，OLS回归中的二次项将捕获异常值。

res = sm.OLS(y2, X).fit()
print(res.params)
print(res.bse)
print(res.predict())

# 估计拟合 RLM 模型:

resrlm = sm.RLM(y2, X).fit()
print(resrlm.params)
print(resrlm.bse)

# 绘制一张图用于比较 OLS 估计值与 robust 估计值:

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111)
ax.plot(x1, y2, 'o', label="data")
ax.plot(x1, y_true2, 'b-', label="True")
prstd, iv_l, iv_u = wls_prediction_std(res)
ax.plot(x1, res.fittedvalues, 'r-', label="OLS")
ax.plot(x1, iv_u, 'r--')
ax.plot(x1, iv_l, 'r--')
ax.plot(x1, resrlm.fittedvalues, 'g.-', label="RLM")
ax.legend(loc="best")

# ### 示例2: 具有真实线性的线性函数
#
# 仅使用线性项和常数拟合一个新的OLS模型:

X2 = X[:, [0, 1]]
res2 = sm.OLS(y2, X2).fit()
print(res2.params)
print(res2.bse)

# 估计拟合 RLM 模型:

resrlm2 = sm.RLM(y2, X2).fit()
print(resrlm2.params)
print(resrlm2.bse)

# 绘制一张图用于比较 OLS 估计值与 robust 估计值::

prstd, iv_l, iv_u = wls_prediction_std(res2)

fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(x1, y2, 'o', label="data")
ax.plot(x1, y_true2, 'b-', label="True")
ax.plot(x1, res2.fittedvalues, 'r-', label="OLS")
ax.plot(x1, iv_u, 'r--')
ax.plot(x1, iv_l, 'r--')
ax.plot(x1, resrlm2.fittedvalues, 'g.-', label="RLM")
legend = ax.legend(loc="best")
