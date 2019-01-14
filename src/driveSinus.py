import csv
import numpy as np

import matplotlib.pyplot as plt



def getLst(lst, coeffs):
    newLst = []
    for i in range(len(lst)):
        val = coeffs[0] * np.sin(coeffs[1] * i + coeffs[2])
        newLst.append(val)

    return newLst


def wrtePlot(t, sinusLst, newSinusLst, path, caption):
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
    plt.savefig(path)


def findSinusCoeffs(lst):
    prevL = lst[0]

    amp0 = max(lst)

    flgDrop = False
    zerosLst = []
    findedZero = -1

    for i in range(len(lst)):
        if (abs(lst[i]) < 0.05):
            if not flgDrop:
                findedZero = i
                flgDrop = True
        if (abs(amp0-abs(lst[i]))<0.2):
            flgDrop = False
            if findedZero!=-1:
                zerosLst.append(int((i+findedZero)/2))
                findedZero = -1



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
    print(zerosLst[0]/ meanPeriod*np.pi)
    #phi0 = zerosLst[0]/ meanPeriod*np.pi
    phi0 = zerosLst[0]+np.pi/2

    amps = []

    # find amplitude
    amp0 = max(lst)
    print("amp: ", amp0)
    flgAddAmp = False

    meanAmps = []

    for l in lst:
        if (l > 0 and amp0 - l < 0.2):
            state = "positive"
            # print("make pos")
            break
        if (l < 0 and -amp0 - l > -0.2):
            state = "negative"
            # print("make neg")
            break

    for l in lst:
        if (l > 0 and amp0 - l < 0.2):
            if state == "negative" and len(amps) > 0:
                meanAmps.append(np.mean(amps))
                #  print("loop mean ", np.mean(amps))
                amps.clear()
            if l > prevL:
                flgAddAmp = True
            else:
                if flgAddAmp:
                    amps.append(l)
                flgAddAmp = False
            state = "positive"

        if (l < 0 and -amp0 - l > -0.2):
            if state == "positive" and len(amps) > 0:
                meanAmps.append(np.mean(amps))
                #   print("loop mean ", np.mean(amps))
                amps.clear()

            #  print("negative")
            if l < prevL:
                flgAddAmp = True
            else:
                if flgAddAmp:
                    amps.append(-l)
                flgAddAmp = False
            state = "negative"

        prevL = l

    # for amp in amps:
    #     print(amp)

    amp0 = np.mean(meanAmps)
    # find frequency
    print("mamp ", amp0)

    return [amp0, omega0, phi0]


def getDistance(lst, newLst):
    sum = 0
    for i in range(len(lst)):
        sum += (lst[i] - newLst[i]) ** 2

    return sum


def readLstFromFile(sourse):
    with open(sourse, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        lst = []
        for row in spamreader:
            try:
                lst.append(float(row[0]))
            except:
                pass
    return lst


def getSQD(sourse):
    sinusLst = readLstFromFile(sourse)
    # sinusLst = sinusLst[:10000]

    coeffs = findSinusCoeffs(sinusLst)
    # newSinusLst = getLst(lst, coeffs)
    newSinusLst = preciseFind(sinusLst, coeffs)

    t = np.arange(0, len(sinusLst))

    return [t, sinusLst, newSinusLst]


def getMeanAmp(sourse):
    sinusLst = readLstFromFile(sourse)
    # sinusLst = sinusLst[:10000]

    coeffs = findSinusCoeffs(sinusLst)
    newSinusLst = getLst(sinusLst, coeffs)

    t = np.arange(0, len(sinusLst))

    return [t, sinusLst, newSinusLst]


def getSQD(sourse, start, end):
    sinusLst = readLstFromFile(sourse)[start:end]
    # sinusLst = sinusLst[:10000]

    coeffs = findSinusCoeffs(sinusLst)
    # newSinusLst = getLst(lst, coeffs)
    newSinusLst = preciseFind(sinusLst, coeffs)

    t = np.arange(start, end)

    return [t, sinusLst, newSinusLst]


def getMeanAmp(sourse, start, end):
    sinusLst = readLstFromFile(sourse)[start:end]
    # sinusLst = sinusLst[:10000]

    coeffs = findSinusCoeffs(sinusLst)
    newSinusLst = getLst(sinusLst, coeffs)

    t = np.arange(start, end)

    return [t, sinusLst, newSinusLst]


def preciseFind(lst, coeffs):
    preciseCoeffs = []
    minDist = -1
    for amp in np.arange(coeffs[0] * 0.8, coeffs[0] * 1.2, coeffs[0] * 0.05):
        # print("loop amp: ",amp)
        for omega in np.arange(coeffs[1] * 0.8, coeffs[1] * 1.4, coeffs[1] * 0.05):
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
