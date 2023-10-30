import numpy as np

def pad_with_zeros(vector, length):
    n = len(vector)
    padded_vector = np.pad(vector, (0, length - n), mode='constant')
    return padded_vector

def fft(x):
    x = np.asarray(x, dtype=complex)
    n = len(x)
    next_pow_2 = int(2 ** np.ceil(np.log2(n)))  # Find the next power of 2
    
    # Pad zeros to x to make its length a power of 2
    padded_x = np.pad(x, (0, next_pow_2 - n), 'constant')
    
    if next_pow_2 <= 2:
        return padded_x
    
    even = fft(padded_x[0::2])
    odd = fft(padded_x[1::2])
    
    w = np.exp(-2j * np.pi * np.arange(next_pow_2) / next_pow_2)
    fft_result = np.concatenate([even + w[:next_pow_2 // 2] * odd, even + w[next_pow_2 // 2:] * odd])
    
    return fft_result

def ifft(x):
    x = np.asarray(x, dtype=complex)
    n = len(x)
    
    if n <= 1:
        return x
    
    even = ifft(x[0::2])
    odd = ifft(x[1::2])
    
    w = np.exp(2j * np.pi * np.arange(n) / n)
    ifft_result = np.concatenate([even + w[:n // 2] * odd, even + w[n // 2:] * odd])
    
    return ifft_result / n

def convolution(x, y):
    n = len(x) + len(y) - 1
    x_padded = pad_with_zeros(x, n)
    y_padded = pad_with_zeros(y, n)
    result = np.fft.ifft(np.fft.fft(x_padded) * np.fft.fft(y_padded))
    return result[:n]


#Testing FFT, IFFT, CONV Functions 

x = [2, 3, -1, 0, 4]
y = [1, 2, 3, 1, 12]

fft_result = fft(x)
ifft_result = ifft(fft_result)
convolution_result = convolution(x, y)

print("FFT result:", fft_result)
print("IFFT result:", ifft_result)
print("Convolution result:", convolution_result)

