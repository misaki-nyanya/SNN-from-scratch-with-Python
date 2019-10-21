# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import scipy.special as sps

np.random.seed(seed=0)

dt = 1e-3; T = 1; nt = round(T/dt) # シミュレーション時間
n_neurons = 10 # ニューロンの数

fr = 30 # ガンマスパイクの発火率(Hz)
k = 12 # k=1のときはポアソン過程に一致
theta = 1/(k*(fr*dt)) # fr = 1/(k*theta)
isi = np.random.gamma(shape=k, scale=theta,
                      size=(int(nt*1.5/fr), n_neurons))
spike_time = np.cumsum(isi, axis=0) # ISIを累積
spike_time[spike_time > nt - 1] = -1 # ntを超える場合を0に
spike_time = spike_time.astype(np.int32) # float to int
spikes = np.zeros((nt, n_neurons)) # スパイク記録変数
for i in range(n_neurons):    
    spikes[spike_time[:, i], i] = 1
spikes[0] = 0 # (spike_time=0)の発火を削除
print("Num. of spikes:", np.sum(spikes))
print("Firing rate:", np.sum(spikes)/(n_neurons*T))

# 描画
plt.figure(figsize=(5, 5))
t = np.arange(nt)*dt
plt.subplot(2,1,1)
count, bins, ignored = plt.hist(isi.flatten(),
                                50, density=True,
                                color="gray", alpha=0.5)
y = bins**(k-1)*(np.exp(-bins/theta) / (sps.gamma(k)*theta**k))
plt.plot(bins, y, linewidth=2, color="k")
plt.title('$k=$'+str(k)) 
plt.xlabel('ISI (ms)') 
plt.ylabel('Probability density') 

plt.subplot(2,1,2)
for i in range(n_neurons):    
    plt.plot(t, spikes[:, i]*(i+1), 'ko', markersize=2,
             rasterized=True)
plt.xlabel('Time (s)')
plt.ylabel('Neuron index') 
plt.xlim(0, T)
plt.ylim(0.5, n_neurons+0.5)
plt.tight_layout()
plt.savefig("gamma_process2.pdf", dpi=300)
plt.show()
    
