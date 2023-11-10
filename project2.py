import cmath
import math
import random

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

def trim_zeros(vector):
    while vector[-1] == 0:
        vector.pop()
            
    return vector


#Problem 2: Taken from the handout
def divide(A,B):   #A is a vector of length n and B is a vector of length m where m<=n
   
    n = len(A) + len(B) - 1
    next_pow_2 = int(2 ** math.ceil(math.log2(n)))
    A = pad_with_zeros(A,n) #May need to fix, need to ask what Len is passed
    B = pad_with_zeros(B,n)

    f1 = fft(A)
    f2 = fft(B)

    #Have python choose some small number to add to A in case f2 is a 0
    constant = random.uniform(0, 1e-10)
    A_perturbed = []
    for i in range(len(A)):
        A_perturbed.append(A[i] + constant)

    length = len(f1)
    f3 = [0] * length  #third vector initalized with length of f1
    
    j = 0
    while (j <= length-1):
        if f2[j] == 0.0:
            f3[j] = A_perturbed[j]
        else:    
            f3[j] = f1[j]/f2[j]
        j += 1
    f4 = ifft(f3)

    f4 = trim_zeros(f4) #Write function to trim 0's from IFFT before returning f4 to the user!

    return f4

#Read file from user    
def inp_file(filename):
    extracted_values = []
    #filename = "/Users/franco/Documents/GitHub/CS415-Probject2/p2-test-case1.txt"
    with open(filename, 'r') as f:
        lines = f.readlines()

    for line in lines:
        # Extract individual values from the array declaration
        for value in line.strip('[]').split(','):
            extracted_values.append(float(value))
           

    #print(extracted_values)
    return extracted_values



#Will take an input from a user
def main():
    print("\t---Questions---")
    print("1\t2\t3\t4")
    quest = int(input("Enter a problem to solve: "))

    match quest:
        case 1:
            name = input("Enter the name of the file to read: ")
            F = inp_file(name)
            print(find_coefficients(F))
        case 2:
            name = input("Enter the name of the first file to read: ")
            second = input("Enter the name of the second file to read: ")
            name = "/Users/franco/Documents/GitHub/CS415-Project2/p2-test-case2a.txt"
            second = "/Users/franco/Documents/GitHub/CS415-Project2/p2-test-case2b.txt"
            F = inp_file(name)
            F2 = inp_file(second)
            result = divide(F,F2) 
            print("Divide result:\n ", result)

        case 3:
            print("3")
        case 4:
            print("Goodbye")


    """
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


    """
    TO DO:
        Implement all of problem 3
            
        Last things:
            Reread all of the project details to make sure they were followed correctly. If there are any quesitons ask in Piazza 
            Ravi is here to help and would rather you ask then not answer the question!

        Final thing:
            Output CPU time after each problem is called. See time.process_time



            How to read file
            /Users/franco/Documents/GitHub/p2-test-cases.txt

    """


main()