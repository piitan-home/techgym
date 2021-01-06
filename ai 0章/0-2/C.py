from _import_ import np, display

inf_a = 9999999999
inf_b = 1234567890
inf_c = 4294967296 - 1

ar = np.array([[1, 0, 0], [inf_a, 1, 0], [inf_b, inf_c, 1]])  # 下三角行列
det = np.linalg.det(ar)  # 行列式

display(det)
display(det == 1)

det = np.linalg.det(ar.T)

display(det)
display(det == 1)