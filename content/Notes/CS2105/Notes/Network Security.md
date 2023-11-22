>[!note]
>Security is not constraint to a single layer. It can be at any layer. For example, `https` is a network security feature at the Application Layer

Suppose there is *Alice* and *Bob* who want to communicate over a public channel. If there is *Trudy* (intruder) may:
1. **Eavesdrop**
2. **Delete**
3. **Add messages**
4. **Impersonation** : *spoof* source address in packet
5. **Hijacking** : *take over* ongoing connection by removing the sender or receiver, inserting oneself in place
6. **Denial of service** : *prevent* service from being used by others

*Alice* or *Bob* may **repudiate**. (ie they can deny sending a message)

As such, we say that *Alice* and *Bob* wish to communicate ==securely==.

![[networksecurity-securechannel.png| -s | -center]]

>[!example]
>1. Web browsers/ server for electronic transactions
>2. On-line baking client/ server
>3. DNS servers
>4. Routers exchanging routing table updates

----
### Confidentiality
>[!note]
>Only the sender and intended receiver should *understand* message contents

### Authentication
>[!note]
>Sender, receiver want to *confirm identity* of each other

### Message integrity
>[!note]
>Sender and receiver want to ensure that message is not *altered* (in transit or afterwards) without detection
---
# Basics of cryptography
Cryptographic techniques allow sender to *disguise* the message (*plain text*). The encryption algorithm generates a *cipher text* and the decryption algorithm decrypts to generate *plain text*.

To differentiate senders, a *key*, $K_A$, is used as an input parameter to the encryption and $K_B$ as an input parameter for decryption algorithm .

## Types of cryptography
Based on the values of the keys there are 2 types of cryptographic algorithm

### Symmetric key
>[!note]
>Alice and Bob share the same (symmetric) key, $K_s$

![[networksecurity-ciphertext.png| -s | -center]]

Alice and Bob needs to agree on the *key value* prior to communication via some other **secure** means.

>[!example]- Caesar’s cipher
>This is a form of substitution cipher, each alphabet is right fixed-shift by $n$.
>
>Then, the decryption algorithm is left shift by $n$. The encryption key is $n$ and it has 25 possible values.

>[!example]- Monoalphabetic cipher
>Another substitution cipher based on a pre-defined permutation and the decryption is the inverse of the permutation.
>
>The key is the permutation mapping from set of 26 alphabets. There are $26!$ keys.
>
>Can be broken with statistical analysis based on the most frequent letters

For monoalphabetic cipher, use ==polyalphabetic encryption==.

In this encryption, we use $n$ substitution ciphers and define a cycling pattern. Then, the key becomes the cycling pattern and the mappers. Therefore, there are $n + 1$ elements in the key.

#### Block ciphers
The message to be encrypted is processed in blocks of $K$ bits. For example, if $K = 64$, the message is broken into 64-bit blocks. To encode a block, the cipher uses a one-to-one mapping.

The number of keys is $2^K !$ → brute force is impossible.

==Data Encryption Standard==
- 56-bit symmetry key, 64-bit block
- 3DES : encrypt 3 times with 3 different keys

==Advanced Encryption Standard==
- Symmetric-key NIST standard
- 128 bit blocks, 128, 192, or 256 bit keys

>[!caution] Major drawback
>Requires sender, receiver to know and agree on a shared secret key

#### Public key cryptography
- Encryption algorithm on the sender uses a *public* key $K_B^+$ which belongs to the receiver and is known to *all*.
- The receiver uses a *private* key, $K_B^-$ which also belongs to the receiver.

![[networksecurity-ciphertextkeys.png| -s | -center]]

1. The algorithms must be *invertible*.
2. Given the public key, it should be impossible to compute private key (Therefore, encryption needs to be more complex)

### RSA
>[!note]- Modulo math
![[networksecurity-modulomaths.png| -s | -center]]

- Read the *message* just a bit pattern and uniquely represent as an *integer* number
- Thus, encrypting a message is equivalent to encrypting a number

#### Creating public, private key pair
1. Choose 2 large prime numbers $p, q$
2. Compute $n = pq, \enspace z = (p-1)(q-1)$
3. Choose $e < n$ that has no common factors with $z$ ($e$ and $z$ are relatively prime)
4. Choose $d$ such that $ed - 1$ is exactly divisible by $z$ $\implies ed \mod z = 1$
5. *Public* key is $(n, e)$ and *private* key is $(n, d)$

Note that generating these numbers are polynomial time operations.

#### Encryption, decryption
Suppose we have $(n, e)$ and $(n, d)$ as computed above

1. To encrypt the message $m$, $c = m^e \mod n$
2. To decrypt $m = c^d \mod n$

>[!example]
>1. $p = 5, q = 7 \implies n = 35, z = 24$
>2. $e = 5$
>3. $d = 29$
>4. Public = $(35, 5)$ and private = $(35, 29)$
>5. Suppose the bit pattern `00001100` is the integer $m = 12$
>6. **Encrypt**: $c = m^e \mod n = 17$
>7. **Decrypt**: $m = c^d \mod n = 12$

Since the encryption and decryption is via exponentiation, we can use public key followed by private key or private key followed by public key to give the same results.

>[!caution]
>Exponentiation in RSA is computationally intensive.

#### Combining with DES
1. Select a key $K_s$
2. Use RSA to transfer $K_s$
3. Use $K_s$ as the symmetric key in DES for encrypting data for this session

The symmetric key $K_s$ is called the *session key*

In other words, we are encrypting only the key with RSA instead of the entire message. Then, we use DES to communicate the message.

>[!success] This achieves [[Network Security#Confidentiality]]

---

# Cryptographic hash function

>[!note] Hash function
>If a function $H$ that takes an input $m$ and produces fixed-sized message digest called *fingerprint*

#### Cryptographic hash function
- A small change in the input should result in a large change in the hash output

A hash function such that it is computationally *infeasible* to find any two different messages $x$ and $y$ such that $H(x) = H(y)$.

This property means that it is computationally infeasible for an intruder to substitute message for another to give the same hash value.

| Hash function | Msg digest in bits |
| ------------- | ------------------ | 
| MDA-5         | 128                |  
| SHA-1         | 160                |

#### Message authentication code
The sender and receiver share a auth key *s*.

To ensure message integrity, augment the message as $(m, H(m + s))$.

![[networksecurity-authentication.png| -s | -center]]

>[!success] This achieves [[Network Security#Message integrity]]
---

# Digital signatures

- Sender digitally *signs* document, establishing the sender is the document owner/ creator.

The signature must be:
1. **Verifiable** : Recipient can check if the signature and the message was generated by Bob
2. **Unforgeable** : No one other than the sender should be able to generate the message $\implies$ signature should be a function of the message

Sender signs by encrypting with his private key $K_B^-$, creating the signature $K_B^-(m)$. The sender sends $(m, K_B^-(m))$.

When receiver receives the message, it verifies $m$ signed by the sender by applying sender’s public key, then check if it is indeed $m$.

>> $K_B^+(K_B^-(m)) = m$

Receiver can thus verify that:
1. Sender signed $m$
2. No one else signed $m$
3. Sender signed $m$ and not $m’$

Non-repudiation
1. Receiver can take $m$ and signature $K_B^-(m)$ to court and prove that sender signed $m$
---
## Optimisation
>[!note]
>It is computationally expensive to public-key-encrypt long messages

1. Apply the hash function $h$ on large message $m$ to get a *fixed size* message digest $h(m)$
2. Then, use the private key to sign the message digest

Generate hash value for a large message.

![[networksecurity-digitalsignature.png| -s | -center]]

---
## Public key certification

The receiver cannot regenerate the signature as there is no *shared authentication key*. However, intruder can use their public key and claim as someone else’s public key.

Then, we need a *certification authority* who maintain a public database of everyone’s public key. Anyone who receives a public key will access this database for $K_B^+$.

To prevent intruders from intercepting communication with CA, CA signs its messages.
Then, it makes the public key a universal knowledge and maintain a list of CAs trusted a priori.

---

>[!success] This achieves [[Network Security#Authentication]] and achieves [[Network Security#Message integrity]] as a side effect.

---
# Breaking encryption scheme
- Ciphertext only attack : intruder has ciphertext that can be analysed
- Known-plaintext attack : intruder has plaintext corresponding to ciphertext
- Chosen-plaintext attack : intruder can get ciphertext for chosen plaintext

---

>[!info] Not part of syllabus
>Access and availability : Services must be accessible and available to users
>
>Basically, firewall.

---
