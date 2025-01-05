# Cryptography
Exploring the security of Learning With Errors crypto system

## Task 1 - Implementing Learning With Errors

### Key Generation
1. Choose a matrix A uniformly at random from $\mathbb{Z}_q^{m \times n}$
2. Choose s uniformly at random from $\mathbb{Z}_q^n$
3. Sample e from a noise distribution $\chi^m$
4. Compute $b = A \cdot s + e$
5. Return $(A, b)$ as the public key and $s$ as the private key.

### Encryption

To encrypt a plaintext bit $\text{pt}$:

1. Choose $r$ uniformly at random from $\mathbb{Z}_2^m$
2. Compute $a'^\top = r^\top \cdot A$
3. Compute $b' = r^\top \cdot b + \text{pt} \cdot \frac{q}{2}$
4. Return $(a', b')$ as the ciphertext

### Decryption

To decrypt the ciphertext $(a', b')$:

1. Compute $v = a'^\top \cdot s$
2. Compute $m' = b' - v$
3. $\text{ If } m' \text{ is closer to } 0 \text{ than } \frac{q}{2} \text{ (mod q)} \text{ then pt} = 0; \text{ else pt } = 1$

### Encrypt function:
A function encrypt(plaintext, public key, q) which, given a plaintext and a public key of compatible size, and an integer q, returns a correct ciphertext. The plaintext will be given as a NumPy integer array consisting of 0s and 1s, which should be interpreted as a sequence of bits to encrypt (using the same key, but different random r, for each bit). The public Key will be given as a ab pair of NumPY integer arrays of appropriate sizes with entries (a',b') are pairs of numPY integer array a' and integer b' again with entries between 0 and q - 1.

### Decryption function:
A function decrypt(ciphertext, private key, q) which, given a ciphertext and private key of compatible sizes, and an integer q, returns the correct plaintext, with the same data types as in the encryption function.

## Task 2 - Attacking ‘Learning Without Errors’

Alice and Bob wish to communicate secretly and in a quantum-secure fashion. Since they do not like errors, they design their own cryptosystem, which they call ‘Learning Without Errors’. This takes the specification of Learning With Errors above, but sets the error distribution $x$ to always be 0.

### Attack function:
Design and implement a function crack1(ciphertext, public key, q) which, given a ciphertext, returns the correct plaintext (i.e. can decode the ciphertext using only the public key and not the private key) when $x$ is always 0.

## Task 3 - Attacking ‘Learning With A Few Errors’

To improve security, Alice and Bob switch to a non-zero error distribution $x$. However, they choose a distubution which is 1 or -1 with low probability, and is otherwise 0. your task is to devise an attack on their cryptosystem which exploits the fact that there are few errors.

### Attack function:
Design and implement a function crack2(ciphertext, public key, q) which, given a ciphertext, returns the correct plaintext, when $x$ is almost 0.

## Task 4 - Attacking ‘Learning With Errors’

Finally, Alice and Bob switch to a more appropriate choice of $x$, and use the standard specification of Learning With Errors. Your task is again to attack their cryptosystem.

### Attack function:
Design and implement a function crack3(ciphertext, public key, q) which, given a ciphertext, returns the correct plaintext.
