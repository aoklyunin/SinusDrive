from src.driveSinus import getSQD, wrtePlot, getMeanAmp


def getResult(source):
    res = getSQD('../drive_data/' + source + '.csv', 20000, 40000)
    wrtePlot(res[0], res[1], res[2], '../imgs/sqd_' + source + '.png', "sqd_" + source)
    res = getMeanAmp('../drive_data/' + source + '.csv', 20000, 40000)
    wrtePlot(res[0], res[1], res[2], '../imgs/mean_amplitude_' + source + '.png', "mean_amplitude_" + source)


getResult("4-1 CSV")
# getResult("4-2 CSV")
# getResult("5 2 csv")
# getResult("6")
