import csv
import numpy as np

import matplotlib.pyplot as plt


def getDist(lstA, lstB):
    sum = 0
    for i in range(len(lstA)):
        sum += (lstA[i] - lstB[i]) * (lstA[i] - lstB[i])

    return sum


def findRealSinus(lst):
    amp0 = max(lst)
    phi0 = -np.pi
    omega0 = 0.00001

    ampMin = amp0
    phiMin = phi0
    omegaMin = omega0
    lstMin = []
    minSum = -1

    # for ampDelta in np.arange(-0.02, 0.02, 0.01):
    ampDelta = 0
    for phiDelta in np.arange(0, np.pi, 0.2):
        for omegaDelta in np.arange(0, 0.003, 0.00001):

            newLst = []
            for i in range(len(lst)):
                amp = amp0 + ampDelta
                omega = omega0 + omegaDelta
                phi = phi0 + phiDelta
                newLst.append(amp * np.sin(omega * i + phi))
            sum = getDist(lst, newLst)

            print(ampDelta, " ", phiDelta, " ", omegaDelta, " ", sum)
            if minSum == -1:
                minSum = sum
                lstMin = newLst
            elif sum < minSum:
                minSum = sum
                lstMin = newLst


    return lstMin

with open('../drive_data/4-1 CSV.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    lst = []
    for row in spamreader:
        try:
            lst.append(float(row[0]))
        except:
            pass
    # for l in lst:
    #     print(l)

sinusLst = lst[:10000]
# sinusLst = []
# for i in range(int(len(lst)/20)):
#     sinusLst.append(lst[i*20])

newSinusLst = findRealSinus(sinusLst)

dt = 0.01
t = np.arange(0, len(sinusLst))
# print(len(t))
# print(len(sinusLst))
# fig, axs = plt.subplots(2, 1)

plt.plot(t, sinusLst, t, newSinusLst)

# axs[0].plot(t, sinusLst, t, sinusLst)
#
# axs[0].set_xlim(0, 2)
# axs[0].set_xlabel('time')
# axs[0].set_ylabel('mes and approx')
# axs[0].grid(True)

# cxy, f = axs[1].cohere(s1, s2, 256, 1. / dt)
# axs[1].set_ylabel('coherence')

# fig.tight_layout()
plt.show()
