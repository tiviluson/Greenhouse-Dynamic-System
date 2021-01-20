import  numpy as np


MVFogAir = None
MVBlowAir = None
MVAirThermalScreen = None
MVAirTop = None
MVAirOut = None
MVTopOut = None
MVTopCoverInternal = None
MVAirMech = None
capVPAir = None

def Calculate_MVFogAir(uFog, phiFog, aFlr) :
    return uFog * phiFog / aFlr

def Calculate_hBlowAir(HEC12, tBlow, tAir) :
    return HEC12 * (tBlow - tAir)

def Calculate_MVBlowAir(etaHeatVap, hBlowAir) :
    return etaHeatVap * hBlowAir

def Calculate_MVAirThermalScreen(sMV12, HEC12, VPAir, VPThermalScreen) :
    partone = 1 / (1 + np.exp(sMV12 * (VPAir - VPThermalScreen)))
    parttwo = 6.4 * (10 ** (-9)) * HEC12 * (VPAir - VPThermalScreen)
    return partone * parttwo

def Calculate_MVAirTop(mWater, RGas, fThermalScreen, VPAir, VPTop, tAir, tTop) :
    return (mWater / RGas) * fThermalScreen * ((VPAir / tAir) - (VPTop / tTop))

def Calculate_MVAirOut(mWater, RGas, fVentSide, VPAir, VPOut, tAir, tOut) :
    return (mWater / RGas) * fVentSide * ((VPAir / tAir) - (VPOut / tOut))

def Calculate_MVAirOutPad(fPad, mWater, RGas, VPAir, tAir) :
    return fPad * (mWater / RGas) * (VPAir / tAir)

def Calculate_MVTopOut(mWater, RGas, fVentRoof, VPTop, VPOut, tTop, tOut) :
    return (mWater / RGas) * fVentRoof * ((VPTop / tTop) - (VPOut / tOut))

def Calculate_MVTopCoverInternal(sMV12, HEC12, VPTop, VPCoverInternal) :
    partone = 1 / (1 + np.exp(sMV12 * (VPTop - VPCoverInternal)))
    parttwo = 6.4 * (10 ** (-9)) * HEC12 * (VPTop - VPCoverInternal)
    return partone * parttwo

def Calculate_MVAirMech(sMV12, HEC12, VPAir, VPMech) :
    partone = 1 / (1 + np.exp(sMV12 * (VPAir - VPMech)))
    parttwo = 6.4 * (10 ** (-9)) * HEC12 * (VPAir - VPMech)
    return partone * parttwo

def Calculate_capVPAir(mWater, hAir, RGas, tAir) :
    return (mWater * hAir) / (RGas * tAir)

def Calculate_capVPTop(mWater, hTop, RGas, tTop) :
    return (mWater * hTop) / (RGas * tTop)

def Calculate_VPAirDot(MVCanAir, MVPadAir, MVFogAir, MVBlowAir, MVAirThermalScreen, MVAirTop, MVAirOut, MVAirOutPad, MVAirMech, capVPAir) :
    return (MVCanAir + MVPadAir + MVFogAir + MVBlowAir - MVAirThermalScreen - MVAirTop - MVAirOut - MVAirOutPad - MVAirMech) / capVPAir

def Calculate_VPTopDot(MVAirTop, MVTopCoverInternal, MVTopOut, capVPTop) :
    return (MVAirTop - MVTopCoverInternal - MVTopOut) / capVPTop

def Calculate_MVCanAir(VECCanAir, VPCan, VPAir) :
    return VECCanAir * (VPCan - VPAir)

def Calculate_VECCanAir(rhoAir, cPAir, LAI, deltaH, gamma, rB, rS) :
    return (2 * rhoAir * cPAir * LAI) / (deltaH * gamma * (rB + rS))

def Calculate_rS(rSMin, rfFRCan, rfCO2AirPpm, rfVPCanMinusVPAir) :
    return rSMin * rfFRCan * rfCO2AirPpm * rfVPCanMinusVPAir

def Calculate_rfFRCan(rCan, cEvap1, cEvap2) :
    return (rCan + cEvap1) / (rCan + cEvap2)

def Calculate_rfCO2AirPpm(cEvap3, etaMgPpm, CO2Air) :
    return 1 + cEvap3 * ((etaMgPpm * CO2Air - 200) ** 2)

def Calculate_rfVPCanMinusVPAir(cEvap4, VPCan, VPAir) :
    return 1 + cEvap4 * (VPCan - VPAir)

def Calculate_cEvap3(cDayEvap3, sRS, cNightEvap3):
    return (cDayEvap3 * (1 - sRS) + cNightEvap3 * sRS)

def Calculate_cEvap4(cDayEvap4, sRS, cNightEvap4):
    return (cDayEvap4 * (1 - sRS) + cNightEvap4 * sRS)

def Calculate_MVPadAir(rhoAir, fPad, etaPad, xPad, xOut) :
    return rhoAir * fPad * (etaPad * (xPad - xOut) + xOut)
