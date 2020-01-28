import numpy as np
import math

def GetPlaneEquationWithAngle(focalLength,Yaw,Pitch):
    cosineofYaw=float('%.20f' % math.pow(math.cos(math.radians(Yaw)),2))
    cosineofPitch=float('%.20f' % math.pow(math.cos(math.radians(Pitch)),2))
    coefficient=np.array([[1,1,1],[cosineofYaw,cosineofYaw-1,cosineofYaw],[cosineofPitch,cosineofPitch,cosineofPitch-1]])
    equilibrium=np.array([math.pow(focalLength,2),0,0])
    result = np.linalg.solve(coefficient, equilibrium)

    print result

GetPlaneEquationWithAngle(5,0,90)
