import csv
import numpy as np

import matplotlib.pyplot as plt


def getLst(lst, coeffs):
    newLst = []
    for i in range(len(lst)):
        val = coeffs[0] * np.sin(coeffs[1] * i + coeffs[2])
        newLst.append(val)

    return newLst


def findSinusCoeffs(lst):
    # find amplitude
    amp0 = max(lst)
    # find frequency

    flgDrop = False
    zerosLst = []
    for i in range(len(lst)):
        if (abs(lst[i]) < 0.05):
            if not flgDrop:
                zerosLst.append(i)
                flgDrop = True
        else:
            flgDrop = False

    periodsLst = []
    for i in range(len(zerosLst) - 1):
        if zerosLst[i + 1] - zerosLst[i] > 100:
            periodsLst.append((zerosLst[i + 1] - zerosLst[i]) / (np.pi))

    periodSum = 0
    for period in periodsLst:
        periodSum += period

    meanPeriod = periodSum / len(periodsLst)
    omega0 = 1 / meanPeriod

    # find phi0
    phi0 = -np.pi

    phi0 = zerosLst[0] - np.pi / 2

    return [amp0, omega0, phi0]


def getDistance(lst, newLst):
    sum = 0
    for i in range(len(lst)):
        sum += (lst[i] - newLst[i]) ** 2

    return sum


def getSQDPic(sourse, target, caption):
    with open(sourse, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        lst = []
        for row in spamreader:
            try:
                lst.append(float(row[0]))
            except:
                pass

    # sinusLst = lst[:10000]
    sinusLst = lst

    coeffs = findSinusCoeffs(sinusLst)
    # newSinusLst = getLst(lst, coeffs)
    newSinusLst = preciseFind(sinusLst, coeffs)

    t = np.arange(0, len(sinusLst))

    fig, axs = plt.subplots(2, 1)
    axs[0].plot(t, sinusLst, t, newSinusLst)
    axs[0].set_xlabel('time')
    axs[0].set_ylabel('mes and approx')
    axs[0].grid(True)

    axs[1].plot(t, newSinusLst)
    axs[1].set_xlabel('time')
    axs[1].set_ylabel('approx')
    axs[1].grid(True)
    fig.suptitle(caption, fontsize=6)
    fig.tight_layout()
    plt.savefig(target)


#   plt.show()


def getMeanAmpPic(sourse, target, caption):
    with open(sourse, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        lst = []
        for row in spamreader:
            try:
                lst.append(float(row[0]))
            except:
                pass

    sinusLst = lst[:10000]
    #sinusLst = lst

    coeffs = findSinusCoeffs(sinusLst)
    newSinusLst = getLst(sinusLst, coeffs)

    t = np.arange(0, len(sinusLst))

    fig, axs = plt.subplots(2, 1)
    axs[0].plot(t, sinusLst, t, newSinusLst)
    axs[0].set_xlabel('time')
    axs[0].set_ylabel('mes and approx')
    axs[0].grid(True)

    axs[1].plot(t, newSinusLst)
    axs[1].set_xlabel('time')
    axs[1].set_ylabel('approx')
    axs[1].grid(True)

    fig.suptitle(caption, fontsize=6)
    fig.tight_layout()
    plt.savefig(target)


# plt.show()


def preciseFind(lst, coeffs):
    preciseCoeffs = []
    minDist = -1
    for amp in np.arange(coeffs[0] * 0.8, coeffs[0] * 1.2, coeffs[0] * 0.05):
        #print("loop amp: ",amp)
        for omega in np.arange(coeffs[1] * 0.8, coeffs[1] * 1.2, coeffs[1] * 0.05):
            for phi in np.arange(coeffs[2] - np.pi / 40, coeffs[2] + np.pi / 40, np.pi / 80):
                newCoeffs = [amp, omega, phi]

                newLst = getLst(lst, newCoeffs)
                newDist = s = getDistance(lst, newLst)

                # print(newDist, " ", newCoeffs)

                if minDist == -1:
                    minDist = newDist
                    preciseCoeffs = newCoeffs
                elif minDist > newDist:
                    print(newDist, " ", newCoeffs)
                    minDist = newDist
                    preciseCoeffs = newCoeffs

    print("preciseCoeffs: ", preciseCoeffs)
    return getLst(lst, preciseCoeffs)


def getResult(source):
    getSQDPic('../drive_data/' + source + '.csv', '../imgs/sqd_' + source + '.png', "sqd_" + source)
    getMeanAmpPic('../drive_data/' + source + '.csv', '../imgs/mean_amplitude_' + source + '.png',
                  "mean_amplitude_" + source)


# getResult("4-1 CSV")
# getResult("4-2 CSV")
# getResult("5 2 csv")
getResult("6")
