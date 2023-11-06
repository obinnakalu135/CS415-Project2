import cmath
import math

def pad_with_zeros(vector, length):
    n = len(vector)
    padded_vector = vector + [0] * (length - n)
    return padded_vector


def round_complex_number(num):
    # Check if real or imaginary parts are within 0.0001 of an integer
    real = round(num.real) if abs(num.real % 1) < 0.0001 else round(num.real, 4)
    imag = round(num.imag) if abs(num.imag % 1) < 0.0001 else round(num.imag, 4)
    
    # Omit 0 real part or 0 imaginary part
    if real != 0:
        if imag == 0:
            return f"{real}"
        elif imag == 1:
            return f"{real}j"
        else:
            return f"{real}+{imag}j"
    elif imag != 0:
        if imag == 1:
            return "j"
        else:
            return f"{imag}j"
    else:
        return "0"


def fft(x):
    n = len(x)
    next_pow_2 = int(2 ** math.ceil(math.log2(n)))  # Find the next power of 2

    # Pad zeros to x to make its length a power of 2
    padded_x = pad_with_zeros(x, next_pow_2)

    if next_pow_2 == 1:
        return padded_x

    w = [cmath.exp(-2j * cmath.pi * i / next_pow_2) for i in range(next_pow_2)]
    even = fft(padded_x[0::2])
    odd = fft(padded_x[1::2])

    result = [0] * next_pow_2
    for i in range(next_pow_2 // 2):
        result[i] = even[i] + w[i] * odd[i]
        result[i + next_pow_2 // 2] = even[i] - w[i] * odd[i]

    return result


def ifft(x):
    n = len(x)

    if n == 1:  # Base case for recursion
        return x

    w = [cmath.exp(2j * cmath.pi * i / n) for i in range(n)]
    even = ifft(x[0::2])
    odd = ifft(x[1::2])

    ifft_result = [0] * n
    for i in range(n // 2):
        ifft_result[i] = even[i] + w[i] * odd[i]
        ifft_result[i + n // 2] = even[i] - w[i] * odd[i]

    return [(num / n) for num in ifft_result]  # Scale the output by 1/n


def convolution(x, y):
    n = len(x) + len(y) - 1
    next_pow_2 = int(2 ** math.ceil(math.log2(n)))  # Find the next power of 2
    x_padded = pad_with_zeros(x, next_pow_2)
    y_padded = pad_with_zeros(y, next_pow_2)

    fft_x = fft(x_padded)
    fft_y = fft(y_padded)

    fft_product = [fft_x[i] * fft_y[i] for i in range(next_pow_2)]  # Use next_pow_2 instead of n
    convolution_result = ifft(fft_product)

    return convolution_result[:n]

# Testing FFT, IFFT, CONV Functions
x = [0, 1, 0, 1, 0]
y = [1, 0, 1, 0, 1]

fft_result = fft(x)
ifft_result = ifft(fft_result)
convolution_result = convolution(x, y)

print("FFT result:", [round_complex_number(num) for num in fft_result])
print("IFFT result:", [round_complex_number(num) for num in ifft_result])
print("Convolution result:", [round_complex_number(num) for num in convolution_result])

# Problem  1

def multiply_polynomials(polynomials):
    result = [1]
    for polynomial in polynomials:
        result = convolution(result, polynomial)
    return result


def find_coefficients(roots):
    linear_factors = [[1, -root] for root in roots]
    polynomial = multiply_polynomials(linear_factors)
    coefficients = [round_complex_number(num) for num in polynomial]
    return coefficients

roots = [1.4142, -1.4142, -1]

coefficients = find_coefficients(roots)
print("Coefficients:", coefficients)



