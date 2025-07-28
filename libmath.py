def gauss_jordan_inverse(A):
    n = len(A)
    I = [[float(i == j) for i in range(n)] for j in range(n)]
    M = [row[:] for row in A]

    for i in range(n):
        pivot = M[i][i]
        if abs(pivot) < 1e-12:
            for r in range(i+1, n):
                if abs(M[r][i]) > 1e-12:
                    M[i], M[r] = M[r], M[i]
                    I[i], I[r] = I[r], I[i]
                    pivot = M[i][i]
                    break
            else:
                raise ValueError("Matrix is singular and cannot be inverted")

        for j in range(n):
            M[i][j] /= pivot
            I[i][j] /= pivot

        for r in range(n):
            if r != i:
                factor = M[r][i]
                for c in range(n):
                    M[r][c] -= factor * M[i][c]
                    I[r][c] -= factor * I[i][c]

    return I

def mat_mul(A, B):
    result = []
    for i in range(len(A)):
        row = []
        for j in range(len(B[0])):
            s = 0
            for k in range(len(B)):
                s += A[i][k] * B[k][j]
            row.append(s)
        result.append(row)
    return result

def mat_transpose(M):
    return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]

def build_vandermonde(x, degree):
    V = []
    for xi in x:
        row = [1]
        for power in range(1, degree+1):
            row.append(xi**power)
        V.append(row)
    return V

def polynomial_regression(x, y, degree):
    V = build_vandermonde(x, degree)
    V_T = mat_transpose(V)
    V_T_V = mat_mul(V_T, V)
    V_T_y = mat_mul(V_T, [[yi] for yi in y])

    inv = gauss_jordan_inverse(V_T_V)
    a = mat_mul(inv, V_T_y)
    coefficients = [a[i][0] for i in range(len(a))]
    return coefficients

def polynomial_value(coeffs, x):
    y = 0
    for i, c in enumerate(coeffs):
        y += c * (x**i)
    return y

def polynomial_formula_string(coeffs):
    terms = []
    for i, coef in enumerate(coeffs):
        coef_str = f"{coef:.6g}"
        if i == 0:
            terms.append(coef_str)
        else:
            terms.append(f"{coef_str}*x^{i}")
    return " + ".join(terms)
