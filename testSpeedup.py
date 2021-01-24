# 通过图进行加速比测试

from utils.myPrint import PRINT_blue
from utils.myPrint import PRINT_red
from utils.check import checkBool

from calc import calc
from pretreat import read

import pandas as pd
from time import time
import numpy as np

# 写入CSV中
Ns = []
Ms = []
Methods = [] # 由于pd不支持非数字，所以用0123代表上面的方法
CheckCPUs = [] # 都和 dij 的串行相比较
CheckGPUs = []
TimeGPUs = []
TimeCPUs = []

def work(n, m, s):
	"""
	接收一个文件进行读取并进行用时测算
	"""

	temp = np.load(f'./predata/data_{n}_{m}_CSV.npz')
	V, E, W = temp['arr_0'], temp['arr_1'],temp['arr_2']
	CSR = [V, E, W]
	g = read(CSR = CSR)

	methods = ['dij', 'spfa', 'delta']
	res = []

	# GPU  存在一个启动慢问题 所以先启动了
	r = calc(graph = g, useCUDA = True, srclist = s)

	for method in methods:
		g.method = method

		Ns.append(n)
		Ms.append(m)
		Methods.append(method)	

		# CPU 
		t1 = time()
		r = calc(graph = g, useCUDA = False, srclist = s)
		t2 = time()

		res.append(r)
		CheckCPUs.append(checkBool(res[0].dist, r.dist))
		TimeCPUs.append((t2 - t1) * 100000 // 10 / 10000)
		
		# GPU 
		t1 = time()
		r = calc(graph = g, useCUDA = True, srclist = s)
		t2 = time()

		res.append(r)
		CheckGPUs.append(checkBool(res[0].dist, r.dist))
		TimeGPUs.append((t2 - t1) * 100000 // 10 / 10000)


	# edge
	temp = np.load(f'./predata/data_{n}_{m}_edge.npz')
	V, E, W = temp['arr_0'], temp['arr_1'],temp['arr_2']
	edgeSet = [V, E, W]
	g = read(edgeSet = edgeSet, method = 'edge')

	Ns.append(n)
	Ms.append(m)
	Methods.append('edge')	

	# CPU 
	t1 = time()
	r = calc(graph = g, useCUDA = False, srclist = s)
	t2 = time()

	res.append(r)
	CheckCPUs.append(checkBool(res[0].dist, r.dist))
	TimeCPUs.append((t2 - t1) * 100000 // 10 / 10000)
	
	# GPU 
	t1 = time()
	r = calc(graph = g, useCUDA = True, srclist = s)
	t2 = time()

	res.append(r)
	CheckGPUs.append(checkBool(res[0].dist, r.dist))
	TimeGPUs.append((t2 - t1) * 100000 // 10 / 10000)


	# print(res[0].dist)
	# print(res[1].dist)
	# print((res[0].dist == res[1].dist).all())


if __name__ == '__main__':
	
	# 节点数的列表
	# ns = [100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600, 51200]
	ns = [800]

	# 度的列表, 有一个度为 1 可以展示稀疏图
	# ds = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
	ds = [16]

	s = [i for i in range(100)]

	# CSV name 每次运行都是一个新的文件名
	filename = f"./testResult/apsp/test_{str(time())[11:]}.csv"

	for n in ns:
		for d in ds:
			work(n, n * d, s)
			# save
			df = pd.DataFrame({'n':Ns, 'm':Ms, 'method':Methods, 'timeGPU':TimeGPUs, 'checkGPU':CheckGPUs, 'timeCPU':TimeCPUs, 'checkCPU':CheckCPUs})
			# df.to_csv(filename)
			print(df)