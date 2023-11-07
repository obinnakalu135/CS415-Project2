import cmath
import math

#Pads the inputed vector with 0's
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

#implements the fast fourier transfer
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

#implements the inverse fast fourier transfer
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

#does convolution on 2 vectors
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

"""# Testing FFT, IFFT, CONV Functions
x = [0, 1, 0, 1, 0]
y = [1, 0, 1, 0, 1]

fft_result = fft(x)
ifft_result = ifft(fft_result)
convolution_result = convolution(x, y)

print("FFT result:\n", [round_complex_number(num) for num in fft_result],"\n")
print("IFFT result:\n\n", [round_complex_number(num) for num in ifft_result],"\n")
print("Convolution result:\n\n", [round_complex_number(num) for num in convolution_result],"\n")"""

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

"""roots = [1.4142, -1.4142, -1]

coefficients = find_coefficients(roots)
print("Coefficients:", coefficients)"""


#Problem 2: Taken from the handout
def divide(A,B):   #A is a vector of length n and B is a vector of length m where m<=n
    if len(A)>len(B):
        pad_with_zeros(B,len(A)) #May need to fix, need to ask what Len is passed

    f1 = FFT(A)
    f2 = FFT(B)

    length = len(f1)
    f3 = [length]  #third vector initalized with length of f1

    for j in length-1:
        if f2[j] == 0:
            #supposed to add a small constant to some coefficients of A(x)
            print("Add small constant later")
        f3[j] = f1[j]/f2[j]

    f4 = IFFT(f3)
    """
        Write function to trim 0's from IFFT before returning f4 to the user!
    """
    return f4

#Will take an input from a user
def main():
    print("\t---Questions---")
    print("1\t2\t3\t4")
    quest = int(input("Enter a problem to solve: "))

    match quest:
        case 1:
            print("1")
        case 2:
            print("2")
        case 3:
            print("3")
        case 4:
            print("Goodbye")
    # Testing FFT, IFFT, CONV Functions
    x = [0, 1, 0, 1, 0]
    y = [1, 0, 1, 0, 1]

    fft_result = fft(x)
    ifft_result = ifft(fft_result)
    convolution_result = convolution(x, y)

    print("FFT result:\n", [round_complex_number(num) for num in fft_result],"\n")
    print("IFFT result:\n\n", [round_complex_number(num) for num in ifft_result],"\n")
    print("Convolution result:\n\n", [round_complex_number(num) for num in convolution_result],"\n")

    roots = [1.4142, -1.4142, -1]

    coefficients = find_coefficients(roots)
    print("Coefficients:", coefficients)




    """
    TO DO:
        Finish some small code changes for problem two
        Implement all of problem 3

        In main:
            Make it so the match statements call their respective function
            Write a function for file inputs and reading
                Test with Ravi given code
            
        Last things:
            Reread all of the project details to make sure they were followed correctly. If there are any quesitons ask in Piazza 
            Ravi is here to help and would rather you ask then not answer the question!

        Final thing:
            Breath!

    """




main()