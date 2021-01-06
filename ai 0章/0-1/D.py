import numpy as np
import scipy.integrate as integrate


def F(x):
    return 2*x*x + 5*x + 4


result, err = integrate.quad(F, 0, 15)
print(f'積分結果:{result} 誤差:{err}')
