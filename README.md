# Brutus-with-fastecdsa
Brutus with fastecdsa
Brutus Bitcoin Private Key Brute Forcer with fastecdsa

Brutus with fastecdsais a modified copy of Plutus with fastecdsa from imcmurray

Origin: https://github.com/imcmurray/Plutus-fastecdsa

It is modified to generate random private keys until it fits to the given bitcoin wallet address.

To use it, you have to write the bitcoin address in line 14.

Then start it with

python3 brutus.py

Requirements for python ist fastecdsa
Try for example with with pip install fastecdsa

fastecdsa need GMP install. Example for Centos: yum install gmp-devel

Have fun with it and good luck.

