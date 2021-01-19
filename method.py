import numpy as np
import operator
from f2b import *

'''
    dx: function pointer
    h: time step
    init: dictionary of initial value for x_0 and t_0 (x(t_0) = x_0)
    return x(t_0 + h)
'''
def euler(dx, h, init):
    #return init["x"] + h*dx(init)
    return tuple(init["x"][i] + h * dx(init)[i] for i in range(len(init["x"])))

def rk4(dx, h, init):
    k1 = dx(init)
    #k2 = dx({"t": init["t"] + 1/2*h,"x": init["x"] + 1/2*h*k1})
    k2 = dx({"t": init["t"] + 1/2*h, "x": tuple(init["x"][i] + 1/2 * h * k1[i] for i in range(len(init["x"])))})
    #k3 = dx({"t": init["t"] + 1/2*h,"x": init["x"] + 1/2*h*k2})
    k3 = dx({"t": init["t"] + 1/2*h, "x": tuple(init["x"][i] + 1/2 * h * k2[i] for i in range(len(init["x"])))})
    #k4 = dx({"t": init["t"] + h,"x": init["x"] + h*k3})
    k4 = dx({"t": init["t"] + h, "x": tuple(init["x"][i] + h * k3[i] for i in range(len(init["x"])))})
    #return init["x"] + 1/6*h*(k1 + 2*k2 + 2*k3 + k4)
    sum = tuple(k1[i] + 2*k2[i] + 2*k3[i] + k4[i] for i in range(len(k1)))
    #return tuple(map(operator.add, init["x"], tuple(map((1/6*h).__mul__, sum))))
    return tuple(init["x"][i] + 1/6*h*(k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) for i in range(len(init["x"])))

'''
    Inputs for Example 1 and Example 2
'''
def ODE(init):
    return 0.5*init["x"]

def ODE_2(init):
    return init["x"] - init["t"]**2 + 1

def solutionEx1(t):
    return np.exp(0.5*t)

def solutionEx2(t):
    return (t+1)**2 - 0.5*np.exp(t)

'''
    Nicely print info
'''
def printInfo(method, f, solution, h, init, numberOfSteps):
    x_n = init["x"]
    if method == "both":
        printInfo("euler", f, solution, h, init, numberOfSteps)
        printInfo("rk4", f, solution, h, init, numberOfSteps)
    else:
        print("------------------------------------------")
        if method == "euler":
            print("Method: Explicit Euler")
        elif method == "rk4":
            print("Method: Explicit order-4 Runge–Kutta")
        print("n    t     x (est)   x (true)   Error")
        for i in range(numberOfSteps + 1):
            t = init["t"] + i*h
            print("%d | %.2f | %.5f | %.5f | %f" % (i, t, x_n, solution(i*h), abs(x_n - solution(i*h))))
            if method == "euler":
                x_n = euler(f, h, {"t": t, "x": x_n})
            elif method == "rk4":
                x_n = rk4(f, h, {"t": t, "x": x_n})

def printCO2(method, f, h, init, numberOfSteps):
    CO2Air = init["CO2Air"]
    CO2Top = init["CO2Top"]
    if method == "both":
        printCO2("euler", f, h, init, numberOfSteps)
        printCO2("rk4", f, h, init, numberOfSteps)
    else:
        print("------------------------------------------")
        if method == "euler":
            print("Method: Explicit Euler")
        elif method == "rk4":
            print("Method: Explicit order-4 Runge–Kutta")
        print("n    t     CO2AirDot   CO2TopDot")
        for i in range(numberOfSteps + 1):
            t = init["t"] + i*h
            print("%d | %.2f | %.5f | %.5f" % (i, t, CO2Air, CO2Top))
            if method == "euler":
                CO2Air, CO2Top = euler(f, h, {"t": t, "x": (CO2Air, CO2Top)})
            elif method == "rk4":
                CO2Air, CO2Top = rk4(f, h, {"t": t, "x": (CO2Air, CO2Top)})

'''
    Setup and test
'''
'''
pointer = {}
pointer["dx"] = ODE
pointer["dx2"] = ODE_2
pointer["solutionEx1"] = solutionEx1
pointer["solutionEx2"] = solutionEx2
printInfo(method = "both", f = pointer["dx"], solution = pointer["solutionEx1"],
            h = 0.2, init = {"t": 0, "x": 1}, numberOfSteps = 5)
printInfo(method = "both", f = pointer["dx2"], solution = pointer["solutionEx2"],
            h = 0.2, init = {"x": 0.5, "t": 0}, numberOfSteps = 5)
printSummary(method = "both", f = pointer["dx"], h = 0.2, init = {"t": 0, "x": 1}, numberOfSteps = 5)
printSummary(method = "both", f = pointer["dx2"], h = 0.2, init = {"x": 0.5, "t": 0}, numberOfSteps = 5)
'''

pointer = {}
pointer["dx"] = dx
init = {"t": 0, "Constants": Konstants, "CO2Air": CO2Air, "CO2Top": CO2Top, "CO2Out": CO2Out}
printCO2(method = "both", f = pointer["dx"], h = 0.2, init = init, numberOfSteps = 5)
