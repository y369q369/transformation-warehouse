import numpy as np
import math as Math
from math import pi
from math import e
from datetime import datetime, timedelta, timezone

timeformat = '%Y-%m-%d %H:%M:%S'


# 获取太阳能数据
def getSolarData(latitud, Altura, r0, r1, rk, area, eff, panels, lossFactor):
    data = yearHottel(latitud, Altura, r0, r1, rk, area, eff, panels, lossFactor)
    finalData = [yearArr()]

    for y in range(len(data[0])):
        arr = []
        arr.append(data[0][y][0])
        for x in data:
            arr.append(x[y][1])
        finalData.append(arr)
    return finalData


def yearHottel(latitud, Altura, r0, r1, rk, area, eff, panels, lossFactor):
    DAILYARR = []
    for DIA in np.arange(1, 365):
        DAILYARR.append(hottelModel(latitud, Altura, r0, r1, rk, DIA, area, eff, panels, lossFactor))
    return DAILYARR


def hottelModel(latitud, Altura, r0, r1, rk, DIA, area, eff, panels, lossFactor):
    HOURLYARR = []
    a0 = r0 * (0.4237 - 0.00821 * Math.pow(6 - Altura, 2))
    a1 = r1 * (0.5055 - 0.00595 * Math.pow(6.5 - Altura, 2))
    k = rk * (0.2711 - 0.01858 * Math.pow(2.5 - Altura, 2))

    declinacionSolar = 23.45 * Math.sin((2 * Math.pi * (284 + DIA)) / 365)

    WS = Math.pi

    rateOfChange = toRadians(15)
    WSchanging = WS * -1
    Gon = 1367 * (1 + 0.033 * Math.cos(((2 * Math.pi) / 365) * DIA))

    while (WSchanging <= WS):
        HOURLYARR.append(
            getNextRow(WSchanging, latitud, declinacionSolar, a0, a1, k, Gon, area, eff, panels, lossFactor))
        WSchanging += rateOfChange
    HOURLYARR = HOURLYARR[0:-1]
    return HOURLYARR


def getNextRow(WS, latitud, declinacionSolar, a0, a1, k, Gon, area, eff, panels, lossFactor):
    thetaZ = Math.sin(toRadians(latitud)) * Math.sin(toRadians(declinacionSolar)) + Math.cos(
        toRadians(latitud)) * Math.cos(toRadians(declinacionSolar)) * Math.cos(WS)
    try:
        tb = a0 + a1 * Math.pow(Math.e, (k * -1) / thetaZ)
    except Exception as e:
        print(a0, a1, thetaZ)
        return [WS, 0]
    td = 0.271 - 0.2939 * tb
    Gcb = tb * Gon * thetaZ
    Gcd = td * Gon * thetaZ
    Gc = Gcb + Gcd
    Production = 0 if (Gc <= 0) else (Gc * area * eff * panels * (1 - lossFactor)) / 1000000
    return [WS, Production]


# 弧度转角度
def toRadians(angle):
    return angle * (Math.pi / 180)


def yearArr():
    date = datetime(2021, 1, 1)
    end = date + timedelta(days=24)
    array = []
    while (date < end):
        x = date.strftime(timeformat)[4:-5]
        array.append(x)
        date = date + timedelta(days=1)
        tmp_array = ['Time']
        tmp_array.extend(array)
        array = tmp_array
    return array


from datetime import datetime, timedelta, timezone
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # li=getSolarData(31.5, 0.03, 0.95, 0.98, 1.02, 1, 1, 1, 0)
    #
    # print(type(li),len(li))
    # print(type(li[0]),len(li[0]))
    # print(li[2])
    # # s=[ li[i][0] for i in range(24)]
    # for i in range(24):
    #     plt.plot(li[i])
    #     plt.show()
    finalData = [yearArr()]
    print(finalData)
