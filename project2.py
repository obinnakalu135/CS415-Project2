import cmath
import math
import random

#Pads the inputed vector with 0's
def pad_with_zeros(vector, length):
    n = len(vector)
    padded_vector = vector + [0] * (int(length) - n)
    return padded_vector


def round_complex_number(num):
    # Check if real or imaginary parts are within 0.0001 of an integer
    real = round(num.real) if abs(num.real % 1) == 1 else 0
    return real

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
"""

# Problem  1

def find_coefficients(roots):
    n = len(roots) + 1
    coefficients = [0] * n
    coefficients[0] = 1

    for root in roots:
        temp = coefficients.copy()
        for i in range(n):
            coefficients[i] = temp[i] - (root * temp[i - 1] if i >= 1 else 0)
    
    return coefficients[::-1]

"""
roots = [54, 23, 27, 33, 52, 51, 6, 83, 29, 86, 51, 31, 70, 77, 94, 5, 28, 28, 53, 91, 38, 32, 21, 85, 74, 30, 78, 85, 51, 75, 93, 44, 16, 0, 14, 43, 55, 5, 44, 61, 86, 57, 66, 73, 93, 31, 24, 30, 84, 35]


coefficients = find_coefficients(roots)
print("Coefficients:", coefficients)
"""
def trim_zeros(vector):
    while vector[-1] == 0:
        vector.pop()
            
    return vector
"""
def simplify_complex_number(complex_number):

  modulus, argument = cmath.polar(complex_number)
  if modulus == 0:
    modulus = 1e-12
  modulus = round(modulus, 6)
  argument = round(argument, 6)
  simplified_complex_number = cmath.rect(modulus, argument)
  return simplified_complex_number
"""

#Problem 2: Taken from the handout
def divide(A,B):   #A is a vector of length n and B is a vector of length m where m<=n
   
    n = len(A) + len(B) - 1
    next_pow_2 = int(2 ** math.ceil(math.log2(n)))
    A = pad_with_zeros(A,n)
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

    f4 = trim_zeros(f4) 

    return f4


#Problem 3
def signal_input(A,threshold):
    #threshold = 0.01
    A_fft = fft(A)
    """
    Tried taking the abolute value of the array and then taking the real and imaginary numbers out. This does not work as "A_fft is a list"
    
    abs_value = abs(A_fft)
    real_parts = abs_value.real()
    img_parts = abs_value.imag()

    print (real_parts)
    """
    for num in range(len(A_fft)):
        #real_parts = A_fft[num].real()
        if abs(A_fft[num]) < threshold:
            A_fft[num] = 0

    A_ifft = ifft(A_fft)

    return A_ifft


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
            #name = "/Users/franco/Documents/GitHub/CS415-Project2/p2-test-case2a.txt"
            #second = "/Users/franco/Documents/GitHub/CS415-Project2/p2-test-case2b.txt"
            F = inp_file(name)
            F2 = inp_file(second)
            result = divide(F,F2) 
            #print(type(result[0]))
            print("Divide result:\n ", [round_complex_number(num) for num in result])

        case 3:
            name = input("Enter the name of the file to read: ")
            threshold = float(input("Enter the threshold to remove: "))
            #name = "/Users/franco/Documents/GitHub/CS415-Project2/p2-test-case3.txt"
            F = inp_file(name)
            result = signal_input(F, threshold)
            print (result)
        case 4:
            print("Goodbye")


    """
    # Testing FFT, IFFT, CONV Functions
    x = [0, 1, 0, 1, 0]2

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
        Final thing:
            Output CPU time after each problem is called. See time.process_time

            How to read file
            /Users/franco/Documents/GitHub/p2-test-cases.txt

    """


main()