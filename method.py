import numpy as np

'''
    dx: function pointer
    h: time step
    init: dictionary of initial value for x_0 and t_0 (x(t_0) = x_0)
    return x(t_0 + h)
'''
def euler(dx, h, init):
    return init["x"] + h*dx(init)

def rk4(dx, h, init):
    k1 = dx(init)
    k2 = dx({"t": init["t"] + 1/2*h,"x": init["x"] + 1/2*h*k1})
    k3 = dx({"t": init["t"] + 1/2*h,"x": init["x"] + 1/2*h*k2})
    k4 = dx({"t": init["t"] + h,"x": init["x"] + h*k3})
    return init["x"] + 1/6*h*(k1 + 2*k2 + 2*k3 + k4)

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

'''
    Setup and test
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
