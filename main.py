import numpy as np
import pandas as pd
import functions_2b as eq2b
import functions_5 as eq5

CO2AirDot = None
CO2TopDot = None
MCBlowAir = None
MCExtAir = None
MCPadAir = None
MCAirTop = None
fThermalScreen = None
phiCrack = None
MCAirOut = None
fPad = None
fVentRoofSide = None
etaInsectScreen = None
fLeakage = None
fVentSide2Dot = None
fVentSide = None
fVentForced = None
MCTopOut = None
fVentRoof = None
fVentRoof2Dot = None
MCAirCan = None
hCBuf = None

hBlowAir = None
capVPAir = None
capVPTop = None
MVFogAir = None
MVBlowAir = None
MVAirThermalScreen = None
MVAirTop = None
MVAirOut = None
MVAirOutPad = None
MVTopOut = None
MVTopCoverInternal = None
MVPadAir = None
MVCanAir = None
MVAirMech = None
VPAirDot = None
VPTopDot = None
rfFRCan = None
cEvap3 = None
rfCO2AirPpm = None
cEvap4 = None
rfVPCanMinusVPAir = None
rS = None
VECCanAir = None
MVCanAir = None
MVPadAir = None

try:
    cons = pd.read_csv("Constants.csv")
except:
    print("Can't open file")
    quit()

Constants = cons.to_dict('records')[0]

def dx(init) :
    CO2Air = init["x"][0]
    CO2Top = init["x"][1]
    CO2Out = 500
    rhoAir = eq2b.Calculate_rhoAir(Constants['rhoAirZero'], Constants['g'], Constants['mAir'], Constants['hElevation'], Constants['RGas'])
    rhoTop = eq2b.Calculate_rhoTop(Constants['rhoAirZero'], Constants['g'], Constants['mAir'], Constants['hElevation'], Constants['RGas'])

    fThermalScreen = eq2b.Calulate_fThermalScreen(Constants['uThermalScreen'], Constants['kThermalScreen']
    , Constants['tAir'], Constants['tTop'], Constants['g'], Constants['rhoMeanAir'], rhoAir, rhoTop)

    phiCrack = eq2b.Calculate_phiCrack(Constants['L'], Constants['SO'], Constants['rhoMean'], Constants['g'], rhoTop, rhoAir)

    fVentRoofSide = eq2b.Calculate_fVentRoofSide(Constants['cD'], Constants['aFlr'], Constants['uRoof']
    , Constants['uSide'], Constants['aRoof'], Constants['aSide'], Constants['g'], Constants['hSideRoof']
    , Constants['tAir'], Constants['tOut'], Constants['tMeanAir'], Constants['cW'], Constants['vWind'])

    etaInsectScreen = eq2b.Calculate_etaInsectScreen(Constants['zetaInsectScreen'])

    fLeakage = eq2b.Calculate_fLeakage(Constants['cLeakage'], Constants['vWind'])

    fVentSide2Dot = eq2b.Calculate_fVentSide2Dot(Constants['cD'], Constants['uSide'], Constants['aSide']
    , Constants['vWind'], Constants['aFlr'], Constants['cW'])

    fVentSide = eq2b.Calculate_fVentSide(etaInsectScreen, fVentSide2Dot, fLeakage, Constants['uThermalScreen'], fVentRoofSide, Constants['etaSide'], Constants['etaSideThermal'])

    fVentForced = eq2b.Calculate_fVentForced(etaInsectScreen, Constants['uVentForced'], Constants['phiVentForced'], Constants['aFlr'])

    fVentRoof2Dot = eq2b.Calculate_fVentRoof2Dot(Constants['cD'], Constants['uRoof'], Constants['aRoof']
    , Constants['aFlr'], Constants['g'], Constants['hVent'], Constants['tAir'], Constants['tOut']
    , Constants['tMeanAir'], Constants['cW'], Constants['vWind'])

    fVentRoof = eq2b.Calculate_fVentRoof(etaInsectScreen, fVentRoof2Dot, fLeakage, Constants['uThermalScreen'], fVentRoofSide, Constants['etaSide'], Constants['etaRoof'], Constants['etaRoofThermal'])

    hCBuf = eq2b.Calculate_hCBuf(Constants['cBuf'], Constants['cMaxBuf'])

    MCBlowAir = eq2b.Calculate_MCBlowAir(Constants['etaHeatCO2'], Constants['uBlow'], Constants['pBlow'], Constants['aFlr'])
    MCExtAir = eq2b.Calculate_MCExtAir(Constants['uExtCO2'], Constants['phiExtCO2'], Constants['aFlr'])
    MCPadAir = eq2b.Calculate_MCPadAir(Constants['uPad'], Constants['phiPad'], Constants['aFlr'], CO2Out, CO2Air)
    MCAirTop = eq2b.Calculate_MCAirTop(fThermalScreen, CO2Air, CO2Top)
    MCAirOut = eq2b.Calculate_MCAirOut(fVentSide, fVentForced, CO2Air, CO2Out)
    MCTopOut = eq2b.Calculate_MCTopOut(fVentRoof, CO2Top, CO2Out)
    MCAirCan = eq2b.Calculate_MCAirCan(Constants['mCH2O'], hCBuf, Constants['P'], Constants['R'])

    CO2AirDot = eq2b.Calculate_CO2AirDot(MCBlowAir, MCExtAir, MCPadAir, MCAirCan, MCAirTop, MCAirOut, Constants['capCO2Air'])
    CO2TopDot = eq2b.Calculate_CO2TopDot(MCAirTop, MCTopOut, Constants['capCO2Top'])

    '''
    print("CO2AirDot:", CO2AirDot, "- Formula 1")
    print("CO2TopDot:", CO2TopDot, "- Formula 2")
    print("MCBlowAir:", MCBlowAir, "- Formula 3")
    print("MCExtAir:", MCExtAir, "- Formula 4")
    print("MCPadAir:", MCPadAir, "- Formula 5")
    print("MCAirTop:", MCAirTop, "- Formula 6")
    print("fThermalScreen:", fThermalScreen, "- Formula 7")
    print("MCAirOut:", MCAirOut, "- Formula 9")
    print("fVentRoofSide:", fVentRoofSide, "- Formula 10")
    print("etaInsectScreen:", etaInsectScreen, "- Formula 11")
    print("fLeakage:", fLeakage, "- Formula 12")
    print("fVentSide:", fVentSide, "- Formula 13")
    print("fVentForced:", fVentForced, "- Formula 14")
    print("MCTopOut:", MCTopOut, "- Formula 15")
    print("fVentRoof:", fVentRoof, "- Formula 16")
    print("fVentRoof2Dot:", fVentRoof2Dot, "- Formula 17")
    print("MCAirCan:", MCAirCan, "- Formula 18")
    print("hCBuf:", hCBuf, "- Formula 19")
    '''

    return (CO2AirDot, CO2TopDot)

def dxVP(init) :
    CO2Air = init["x"][0]
    CO2Top = init["x"][1]
    CO2Out = 500
    rhoAir = eq2b.Calculate_rhoAir(Constants['rhoAirZero'], Constants['g'], Constants['mAir'], Constants['hElevation'], Constants['RGas'])
    rhoTop = eq2b.Calculate_rhoTop(Constants['rhoAirZero'], Constants['g'], Constants['mAir'], Constants['hElevation'], Constants['RGas'])

    fThermalScreen = eq2b.Calulate_fThermalScreen(Constants['uThermalScreen'], Constants['kThermalScreen']
    , Constants['tAir'], Constants['tTop'], Constants['g'], Constants['rhoMeanAir'], rhoAir, rhoTop)

    phiCrack = eq2b.Calculate_phiCrack(Constants['L'], Constants['SO'], Constants['rhoMean'], Constants['g'], rhoTop, rhoAir)

    fVentRoofSide = eq2b.Calculate_fVentRoofSide(Constants['cD'], Constants['aFlr'], Constants['uRoof']
    , Constants['uSide'], Constants['aRoof'], Constants['aSide'], Constants['g'], Constants['hSideRoof']
    , Constants['tAir'], Constants['tOut'], Constants['tMeanAir'], Constants['cW'], Constants['vWind'])

    etaInsectScreen = eq2b.Calculate_etaInsectScreen(Constants['zetaInsectScreen'])

    fLeakage = eq2b.Calculate_fLeakage(Constants['cLeakage'], Constants['vWind'])

    fVentSide2Dot = eq2b.Calculate_fVentSide2Dot(Constants['cD'], Constants['uSide'], Constants['aSide']
    , Constants['vWind'], Constants['aFlr'], Constants['cW'])

    fVentSide = eq2b.Calculate_fVentSide(etaInsectScreen, fVentSide2Dot, fLeakage, Constants['uThermalScreen'], fVentRoofSide, Constants['etaSide'], Constants['etaSideThermal'])

    fVentForced = eq2b.Calculate_fVentForced(etaInsectScreen, Constants['uVentForced'], Constants['phiVentForced'], Constants['aFlr'])

    fVentRoof2Dot = eq2b.Calculate_fVentRoof2Dot(Constants['cD'], Constants['uRoof'], Constants['aRoof']
    , Constants['aFlr'], Constants['g'], Constants['hVent'], Constants['tAir'], Constants['tOut']
    , Constants['tMeanAir'], Constants['cW'], Constants['vWind'])

    fVentRoof = eq2b.Calculate_fVentRoof(etaInsectScreen, fVentRoof2Dot, fLeakage, Constants['uThermalScreen'], fVentRoofSide, Constants['etaSide'], Constants['etaRoof'], Constants['etaRoofThermal'])

    hCBuf = eq2b.Calculate_hCBuf(Constants['cBuf'], Constants['cMaxBuf'])

    MCBlowAir = eq2b.Calculate_MCBlowAir(Constants['etaHeatCO2'], Constants['uBlow'], Constants['pBlow'], Constants['aFlr'])
    MCExtAir = eq2b.Calculate_MCExtAir(Constants['uExtCO2'], Constants['phiExtCO2'], Constants['aFlr'])
    MCPadAir = eq2b.Calculate_MCPadAir(Constants['uPad'], Constants['phiPad'], Constants['aFlr'], CO2Out, CO2Air)
    MCAirTop = eq2b.Calculate_MCAirTop(fThermalScreen, CO2Air, CO2Top)
    MCAirOut = eq2b.Calculate_MCAirOut(fVentSide, fVentForced, CO2Air, CO2Out)
    MCTopOut = eq2b.Calculate_MCTopOut(fVentRoof, CO2Top, CO2Out)
    MCAirCan = eq2b.Calculate_MCAirCan(Constants['mCH2O'], hCBuf, Constants['P'], Constants['R'])

    CO2AirDot = eq2b.Calculate_CO2AirDot(MCBlowAir, MCExtAir, MCPadAir, MCAirCan, MCAirTop, MCAirOut, Constants['capCO2Air'])
    CO2TopDot = eq2b.Calculate_CO2TopDot(MCAirTop, MCTopOut, Constants['capCO2Top'])

    hBlowAir = eq5.Calculate_hBlowAir(Constants['HEC12'], Constants['tBlow'], Constants['tAir'])

    capVPAir = eq5.Calculate_capVPAir(Constants['mWater'], Constants['hAir'], Constants['RGas'], Constants['tAir'])

    capVPTop = eq5.Calculate_capVPTop(Constants['mWater'], Constants['hTop'], Constants['RGas'], Constants['tTop'])

    rfFRCan = eq5.Calculate_rfFRCan(Constants['rCan'], Constants['cEvap1'], Constants['cEvap2'])

    cEvap3 = eq5.Calculate_cEvap3(Constants['cDayEvap3'], Constants['sRS'], Constants['cNightEvap3'])

    rfCO2AirPpm = eq5.Calculate_rfCO2AirPpm(cEvap3, Constants['etaMgPpm'], CO2Air)

    cEvap4 = eq5.Calculate_cEvap4(Constants['cDayEvap4'], Constants['sRS'], Constants['cNightEvap4'])

    rfVPCanMinusVPAir = eq5.Calculate_rfVPCanMinusVPAir(cEvap4, Constants['VPCan'], Constants['VPAir'])

    rS = eq5.Calculate_rS(Constants['rsMin'], rfFRCan, rfCO2AirPpm, rfVPCanMinusVPAir)

    VECCanAir = eq5.Calculate_VECCanAir(rhoAir, Constants['cPAir'], Constants['LAI'], Constants['deltaH'], Constants['gamma'], Constants['rB'], rS)

    MVCanAir = eq5.Calculate_MVCanAir(VECCanAir, Constants['VPCan'], Constants['VPAir'])
    MVPadAir = eq5.Calculate_MVPadAir(rhoAir, fPad, Constants['etaPad'], Constants['xPad'], Constants['xOut'])
    MVFogAir = eq5.Calculate_MVFogAir(Constants['uFog'], Constants['phiFog'], Constants['aFlr'])
    MVBlowAir = eq5.Calculate_MVBlowAir(Constants['etaHeatVap'], hBlowAir)
    MVAirThermalScreen = eq5.Calculate_MVAirThermalScreen(Constants['sMV12'], Constants['HEC12'], Constants['VPAir'], Constants['VPThermalScreen'])
    MVAirTop = eq5.Calculate_MVAirTop(Constants['mWater'], Constants['RGas'], fThermalScreen, Constants['VPAir'], Constants['VPTop'], Constants['tAir'], Constants['tTop'])
    MVAirOut = eq5.Calculate_MVAirOut(Constants['mWater'], Constants['RGas'], fVentSide, Constants['VPAir'], Constants['VPOut'], Constants['tAir'], Constants['tOut'])
    MVAirOutPad = eq5.Calculate_MVAirOutPad(fpad, Constants['mWater'], Constants['RGas'], Constants['VPAir'], Constants['tAir'])
    MVTopOut = eq5.Calculate_MVTopOut(Constants['mWater'], Constants['RGas'], fVentRoof, Constants['VPTop'], Constants['VPOut'], Constants['tTop'], Constants['tOut'])
    MVTopCoverInternal = eq5.Calculate_MVTopCoverInternal(Constants['sMV12'], Constants['HEC12'], Constants['VPTop'], Constants['VPCoverInternal'])
    MVAirMech = eq5.Calculate_MVAirMech(Constants['sMV12'], Constants['HEC12'], Constants['VPAir'], Constants['VPMech'])

    VPAirDot = eq5.Calculate_VPAirDot(MVCanAir, MVPadAir, MVFogAir, MVBlowAir, MVAirThermalScreen, MVAirTop, MVAirOut, MVAirOutPad, MVAirMech, capVPAir)
    VPTopDot = eq5.Calculate_VPTopDot(MVAirTop, MVTopCoverInternal, MVTopOut, capVPTop)

    print(fPad)
    print(hBlowAir)
    print(capVPAir)
    print(capVPTop)
    print(MVFogAir)
    print(MVBlowAir)
    print(MVAirThermalScreen)
    print(MVAirTop)
    print(MVAirOut)
    print(MVAirOutPad)
    print(MVTopOut)
    print(MVTopCoverInternal)
    print(MVAirMech)
    print(VPAirDot)
    print(VPTopDot)

    return (VPAirDot, VPTopDot)
#dx({"CO2Air": CO2Air, "CO2Top": CO2Top})
