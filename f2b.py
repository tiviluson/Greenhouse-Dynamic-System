import numpy as np
import pandas as pd
import functions_2b as eq

CO2Air = 350
CO2Top = 450
CO2Out = 500

CO2AirDot = None
CO2TopDot = None
MCBlowAir = None
MCExtAir = None
MCPadAir = None
MCAirTop = None
fThermalScreen = None
phiCrack = None
MCAirOut = None
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

try:
    cons = pd.read_csv("Constants.csv")
except:
    print("Can't open file")
    quit()

Konstants = cons.to_dict('records')[0]

def dx(init):
    Constants = Konstants
    CO2Air = init["x"][0]
    CO2Top = init["x"][1]
    CO2Out = 500
    rhoAir = eq.Calculate_rhoAir(Constants['rhoAirZero'], Constants['g'], Constants['mAir'], Constants['hElevation'], Constants['RGas'])
    rhoTop = eq.Calculate_rhoTop(Constants['rhoAirZero'], Constants['g'], Constants['mAir'], Constants['hElevation'], Constants['RGas'])

    fThermalScreen = eq.Calulate_fThermalScreen(Constants['uThermalScreen'], Constants['kThermalScreen']
    , Constants['tAir'], Constants['tTop'], Constants['g'], Constants['rhoMeanAir'], rhoAir, rhoTop)

    phiCrack = eq.Calculate_phiCrack(Constants['L'], Constants['SO'], Constants['rhoMean'], Constants['g'], Constants['rhoTop'], rhoAir)

    fVentRoofSide = eq.Calculate_fVentRoofSide(Constants['cD'], Constants['aFlr'], Constants['uRoof']
    , Constants['uSide'], Constants['aRoof'], Constants['aSide'], Constants['g'], Constants['hSideRoof']
    , Constants['tAir'], Constants['tOut'], Constants['tMeanAir'], Constants['cW'], Constants['vWind'])

    etaInsectScreen = eq.Calculate_etaInsectScreen(Constants['zetaInsectScreen'])

    fLeakage = eq.Calculate_fLeakage(Constants['cLeakage'], Constants['vWind'])

    fVentSide2Dot = eq.Calculate_fVentSide2Dot(Constants['cD'], Constants['uSide'], Constants['aSide']
    , Constants['vWind'], Constants['aFlr'], Constants['cW'])

    fVentSide = eq.Calculate_fVentSide(etaInsectScreen, fVentSide2Dot, fLeakage, Constants['uThermalScreen'], fVentRoofSide, Constants['etaSide'], Constants['etaSideThermal'])

    fVentForced = eq.Calculate_fVentForced(etaInsectScreen, Constants['uVentForced'], Constants['phiVentForced'], Constants['aFlr'])

    fVentRoof2Dot = eq.Calculate_fVentRoof2Dot(Constants['cD'], Constants['uRoof'], Constants['aRoof']
    , Constants['aFlr'], Constants['g'], Constants['hVent'], Constants['tAir'], Constants['tOut']
    , Constants['tMeanAir'], Constants['cW'], Constants['vWind'])

    fVentRoof = eq.Calculate_fVentRoof(etaInsectScreen, fVentRoof2Dot, fLeakage, Constants['uThermalScreen'], fVentRoofSide, Constants['etaSide'], Constants['etaRoof'], Constants['etaRoofThermal'])

    hCBuf = eq.Calculate_hCBuf(Constants['cBuf'], Constants['cMaxBuf'])

    MCBlowAir = eq.Calculate_MCBlowAir(Constants['etaHeatCO2'], Constants['uBlow'], Constants['pBlow'], Constants['aFlr'])
    MCExtAir = eq.Calculate_MCExtAir(Constants['uExtCO2'], Constants['phiExtCO2'], Constants['aFlr'])
    MCPadAir = eq.Calculate_MCPadAir(Constants['uPad'], Constants['phiPad'], Constants['aFlr'], CO2Out, CO2Air)
    MCAirTop = eq.Calculate_MCAirTop(fThermalScreen, CO2Air, CO2Top)
    MCAirOut = eq.Calculate_MCAirOut(fVentSide, fVentForced, CO2Air, CO2Out)
    MCTopOut = eq.Calculate_MCTopOut(fVentRoof, CO2Top, CO2Out)
    MCAirCan = eq.Calculate_MCAirCan(Constants['mCH2O'], hCBuf, Constants['P'], Constants['R'])

    CO2AirDot = eq.Calculate_CO2AirDot(MCBlowAir, MCExtAir, MCPadAir, MCAirCan, MCAirTop, MCAirOut, Constants['capCO2Air'])
    CO2TopDot = eq.Calculate_CO2TopDot(MCAirTop, MCTopOut, Constants['capCO2Top'])

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

#dx({"CO2Air": CO2Air, "CO2Top": CO2Top})
