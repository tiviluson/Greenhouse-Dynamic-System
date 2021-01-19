import numpy as np

# Formula 1
def Calculate_CO2AirDot(MCBlowAir, MCExtAir, MCPadAir, MCAirCan, MCAirTop, MCAirOut, capCO2Air) :
    return (MCBlowAir + MCExtAir + MCPadAir - MCAirCan - MCAirTop - MCAirOut) / capCO2Air

# Formula 2
def Calculate_CO2TopDot(MCAirTop, MCTopOut, capCO2Top) :
    return (MCAirTop - MCTopOut) / capCO2Top

# Formula 3
def Calculate_MCBlowAir(etaHeatCO2, uBlow, pBlow, aFlr) :
    return (etaHeatCO2 * uBlow * pBlow) / aFlr

# Formula 4
def Calculate_MCExtAir(uExtCO2, phiExtCO2, aFlr) :
    return (uExtCO2 * phiExtCO2) / aFlr

# Support Formula 5
def Calculate_fPad(uPad, phiPad, aFlr) :
    return (uPad * phiPad) / aFlr

# Formula 5
def Calculate_MCPadAir(uPad, phiPad, aFlr, CO2Out, CO2Air) :
    return Calculate_fPad(uPad, phiPad, aFlr) * (CO2Out - CO2Air)

# Formula 6
def Calculate_MCAirTop(fThermalScreen, CO2Air, CO2Top) :
    return fThermalScreen * (CO2Air - CO2Top)

# Support Formula 7
def Calculate_rhoAir(rhoAirZero, g, mAir, hElevation, R) :
    return rhoAirZero * np.exp((g * mAir * hElevation) / (293.15 * R))

# Formula 7
def Calulate_fThermalScreen(uThermalScreen, kThermalScreen, tAir, tTop, g, rhoMeanAir, rhoAir, rhoTop) :
    penetrationRate = uThermalScreen * kThermalScreen * (abs(tAir - tTop) ** (2 / 3))
    notCoveredRate = (1 - uThermalScreen) * ((g * (1 - uThermalScreen) * abs(rhoAir - rhoTop) / (2 * rhoMeanAir)) ** (1 / 2))
    return penetrationRate + notCoveredRate

# Formula 8
def Calculate_phiCrack(L, SO, rhoMean, g, rhoTop, rhoAir) :
    firstPart = ((L * SO) / rhoMean)
    secondPart = ((0.5 * rhoMean * SO * g * (rhoTop - rhoAir))**0.5)
    return firstPart * secondPart

# Formula 9
def Calculate_MCAirOut(fVentSide, fVentForced, CO2Air, CO2Out) :
    return (fVentSide + fVentForced) * (CO2Air + CO2Out)

# Formula 10
def Calculate_fVentRoofSide(cD, aFlr, uRoof, uSide, aRoof, aSide, g, hSideRoof, tAir, tOut, tMeanAir, cW, vWind) :
    firstPart = cD / aFlr
    secondPart = ((uRoof**2) * (uSide**2) * (aRoof**2) * (aSide**2)) / ((uRoof**2) * (aRoof**2) + (uSide**2) * (aSide**2))
    thirdPart = (2 * g * hSideRoof * (tAir - tOut)) / tMeanAir
    fourthPart = ((0.5 * (uRoof * aRoof + uSide * aSide))**2) * cW * (vWind**2)
    return (firstPart * (secondPart * thirdPart + fourthPart)**0.5)

# Formula 11
def Calculate_etaInsectScreen(zetaInsectScreen) :
    return zetaInsectScreen * (2 - zetaInsectScreen)

# Formula 12
def Calculate_fLeakage(cLeakage, vWind) :
    if (vWind < 0.25):
        return 0.25 * cLeakage
    else:
        return vWind * cLeakage

# Support Formula 13
def Calculate_fVentSide2Dot(cD, uSide, aSide, vWind, aFlr, cW) :
    return ((cD * uSide * aSide * vWind)/(2 * aFlr)) * np.sqrt(cW)

# Formula 13
def Calculate_fVentSide(etaInsectScreen, fVentSide2Dot, fLeakage, uThermalScreen, fVentRoofSide, etaSide, etaSideThermal) :
    if etaSide >= etaSideThermal :
        result = etaInsectScreen * fVentSide2Dot + 0.5 * fLeakage
    else :
        result = etaInsectScreen * (uThermalScreen * fVentSide2Dot + (1 - uThermalScreen) * fVentRoofSide * etaSide) + 0.5 * fLeakage
    return result

# Formula 14
def Calculate_fVentForced(etaInsectScreen, uVentForced, phiVentForced, aFlr) :
    return (etaInsectScreen * uVentForced * phiVentForced) / aFlr

# Formula 15
def Calculate_MCTopOut(fVentRoof, CO2Top, CO2Out) :
    return fVentRoof * (CO2Top - CO2Out)

# Formula 16
def Calculate_fVentRoof(etaInsectScreen, fVentRoof2Dot, fLeakage, uThermalScreen, fVentRoofSide, etaSide, etaRoof, etaRoofThermal):
    if (etaRoof >= etaRoofThermal):
        return (etaInsectScreen * fVentRoof2Dot + 0.5 * fLeakage)
    else:
        return (etaInsectScreen * (uThermalScreen * fVentRoof2Dot + (1 - uThermalScreen) * fVentRoofSide * etaSide)) + (0.5 * fLeakage)

# Formula 17
def Calculate_fVentRoof2Dot(cD, uRoof, aRoof, aFlr, g, hVent, tAir, tOut, tMeanAir, cW, vWind) :
    partone = (cD * uRoof * aRoof) / (2 * aFlr)
    parttwo = ((g * hVent * (tAir - tOut)) / (2 * tMeanAir) + cW * (vWind ** 2)) ** (1 / 2)
    return partone * parttwo

# Formula 18
def Calculate_MCAirCan(mCH2O, hCBuf, P, R) :
    return (mCH2O * hCBuf) * (P - R)

# Formula 19
def Calculate_hCBuf(cBuf, cMaxBuf) :
    if cBuf > cMaxBuf :
        return 0
    else :
        return 1
