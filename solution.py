import numpy as np
from itertools import combinations, product
import copy

def encrypt(plaintext, public_key, q):
    A, b = public_key
    m, n = A.shape
    ciphertext = []
    for pt in plaintext:
        r = np.random.randint(2, size=(m, 1))
        a_prime = (r.T @ A) % q
        b_prime = ((r.T @ b) + (pt * q // 2)) % q
        ciphertext.append((a_prime.flatten(),  b_prime.item()))

    dtypes = [('a_prime', 'int32', (n,)), ('b_prime', 'int32')]
    ciphertext_np_array = np.array(ciphertext, dtype=dtypes)
    return ciphertext_np_array

def decrypt(ciphertexts, private_key, q):
    plaintext = []

    for a_prime, b_prime in ciphertexts:
        v = abs((a_prime @ private_key)%q)
        dec = (b_prime - v)%q
        
        if dec > q//2:
            dec = q - dec
        result = 0 if dec < (q//4) else 1
        plaintext.append(result)

    return np.array(plaintext)


def crack1(ciphertext, public_key, q):
    A,b = public_key
    m, n = A.shape
    Ab = np.hstack([A, b.reshape(-1, 1)])
    
    #Gaussian elimination
    for i in range(min(m, n)):
        pivot = None
        for row in range(i, m):
            if A[row, i] % q != 0:
                pivot = row
                break
        if pivot is None:
            continue 
        if pivot != i:
            A[[i, pivot]], A[[pivot, i]] = A[[pivot, i]], A[[i, pivot]]
            b[i], b[pivot] = b[pivot], b[i]
        pivot_value = int(A[i, i])  
        inv_pivot_value = pow(pivot_value, -1, q)
        A[i] = (A[i] * inv_pivot_value) % q
        b[i] = (b[i] * inv_pivot_value) % q
        
        for row in range(i+1, m):
            factor = int(A[row, i])  
            A[row] = (A[row] - factor * A[i]) % q
            b[row] = (b[row] - factor * b[i]) % q

    s = np.zeros(n, dtype=int)
    for i in range(n - 1, -1, -1):
        s[i] = b[i] - np.dot(A[i, i+1:], s[i+1:])
        s[i] = int(s[i])  
        s[i] = (s[i] * pow(int(A[i, i]), -1, q)) % q  
    plaintext = []
    for a_prime, b_prime in ciphertext:
        v = abs((a_prime @ s)%q)
        dec = (b_prime - v)%q
        
        if dec > q//2:
            dec = q - dec
        result = 0 if dec < (q//4) else 1
        plaintext.append(result)
    return np.array(plaintext)



def generate_e_vectors(length, max_nonzero):
    e_vectors = []
    e_vectors.append(np.zeros(length))
    for num_nonzero in range(1, max_nonzero + 1):
        for indices in combinations(range(length), num_nonzero):
            for signs in product([-1, 1], repeat=num_nonzero):
                e = np.zeros(length, dtype=int)
                for i, sign in zip(indices, signs):
                    e[i] = sign
                e_vectors.append(e)
    return e_vectors


def crack2(ciphertext,public_key, q):
    A, b = public_key
    x = copy.deepcopy(A)
    m, n = A.shape

    def solve_for_s(b, q):
        A = copy.deepcopy(x)
        m, n = A.shape
        Ab = np.hstack([A, b.reshape(-1, 1)])
        
        for i in range(min(m, n)):
            pivot = None
            for row in range(i, m):
                if A[row, i] % q != 0:
                    pivot = row
                    break

            if pivot is None:
                continue 

            if pivot != i:
                A[[i, pivot]], A[[pivot, i]] = A[[pivot, i]], A[[i, pivot]]
                b[i], b[pivot] = b[pivot], b[i]

            pivot_val = int(A[i, i]) 
            inv_pivot_val = pow(pivot_val, -1, q)
            A[i] = (A[i] * inv_pivot_val) % q
            b[i] = (b[i] * inv_pivot_val) % q

            for row in range(i+1, m):
                factor = int(A[row, i])  
                A[row] = (A[row] - factor * A[i]) % q
                b[row] = (b[row] - factor * b[i]) % q
                
        s = np.zeros(n, dtype=int)
        for i in range(n - 1, -1, -1):
            s[i] = b[i] - np.dot(A[i, i+1:], s[i+1:])
            s[i] = int(s[i])  
            s[i] = (s[i] * pow(int(A[i, i]), -1, q)) % q  
        return s
    
    correct_s=[]
    e = generate_e_vectors(m,5)
    
    for i in e:
        b_adjusted = (b - i) % q
        b_adjusted = np.array(b_adjusted, dtype=int)
        s = solve_for_s(b_adjusted, q).reshape(-1, 1)
        b_new = (x @ s + i.reshape(-1, 1)) % q
        if np.array_equal(b_new.flatten(), b):

            correct_s.append(s)
            break
    
    #print(correct_s)
    plaintext = []
    for a_prime, b_prime in ciphertext:
        v = abs((a_prime @ correct_s[0])%q)
        dec = (b_prime - v)%q
        
        if dec > q//2:
            dec = q - dec

        result = 0 if dec < (q//4) else 1
        plaintext.append(result)
    return np.array(plaintext)

def crack3(ciphertext,public_key, q):
    A,b = public_key 
    m,n = A.shape
    s = [np.array(combination) for combination in product(range(0, q - 1), repeat=n)]
    s = s[1:]  
    correct_s = []
    for i in s:
        i = i.reshape(-1, 1)
        b_new = (A @ i) % q
        if np.all(((np.min(b_new.flatten() - b) >= -1)|(np.max(b_new.flatten() - b) <= 1))):
            correct_s.append(i)
            break
            
    plaintext = []
    for a_prime, b_prime in ciphertext:
        v = abs((a_prime @ correct_s[0])%q)
        dec = (b_prime - v)%q
        
        if dec > q//2:
            dec = q - dec

        result = 0 if dec < (q//4) else 1
        plaintext.append(result)
    return np.array(plaintext)
