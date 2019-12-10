# Plutus Bitcoin Brute Forcer
# Made by Isaac Delly - change for single adress Bruteforce by Christian Hummel
# https://github.com/Isaacdelly/Plutus - https://github.com/diehummel/Brutus-with-fastecdsa
# Added fastecdsa - June 2019 - Ian McMurray

import os
import pickle
import hashlib
import binascii
import multiprocessing
import pickle
from fastecdsa import keys, curve

BTC='17MXanLRMjTy4uYMArdmVJa1ramLp6epk5'

os.mkdir('db')
coinadress ={ BTC }
filename = 'db/00.pickle'
outfile = open(filename,'wb')
pickle.dump(coinadress,outfile)
outfile.close()

DATABASE = r'db/'

def generate_private_key(): 
    """Generate a random 32-byte hex integer which serves as a randomly generated Bitcoin private key.
    Average Time: 0.0000061659 seconds
    """
    return binascii.hexlify(os.urandom(32)).decode('utf-8').upper()

def private_key_to_public_key(private_key):
    """Accept a hex private key and convert it to its respective public key. Because converting a private key to 
    a public key requires SECP256k1 ECDSA signing, this function is the most time consuming and is a bottleneck
    in the overall speed of the program.
    Average Time: 0.0016401287 seconds
    """
    # get the public key corresponding to the private key we just generated
    c = int('0x%s'%private_key,0)
    d = keys.get_public_key(c, curve.secp256k1)
    return '04%s%s'%('{0:x}'.format(int(d.x)), '{0:x}'.format(int(d.y)))

def public_key_to_address(public_key):
    """Accept a public key and convert it to its resepective P2PKH wallet address.
    Average Time: 0.0000801390 seconds
    """
    #print('Wanting to [%s] this to address'%public_key)
    output = []; alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    var = hashlib.new('ripemd160')
    try:
        var.update(hashlib.sha256(binascii.unhexlify(public_key.encode())).digest())
        var = '00' + var.hexdigest() + hashlib.sha256(hashlib.sha256(binascii.unhexlify(('00' + var.hexdigest()).encode())).digest()).hexdigest()[0:8]
        count = [char != '0' for char in var].index(True) // 2
        n = int(var, 16)
        while n > 0:
            n, remainder = divmod(n, 58)
            output.append(alphabet[remainder])
        for i in range(count): output.append(alphabet[0])
        return ''.join(output[::-1])
    except:
        # Nothing
        return -1

def process(private_key, public_key, address, database):
    """Accept an address and query the database. If the address is found in the database, then it is assumed to have a 
    balance and the wallet data is written to the hard drive. If the address is not in the database, then it is 
    assumed to be empty and printed to the user. This is a fast and efficient query.
    Average Time: 0.0000026941 seconds
    """
    
    if address in database:
        with open('plutus.txt', 'a') as file:
            file.write('hex private key: ' + str(private_key) + '\n' +
                       'public key: ' + str(public_key) + '\n' +
                       'address: ' + str(address) + '\n\n')
                       #'WIF private key: ' + str(private_key_to_WIF(private_key)) + '\n' +
    else: 
         print(str(address) + '  -> find ->' + str(database))

def private_key_to_WIF(private_key):
    """Convert the hex private key into Wallet Import Format for easier wallet importing. This function is 
    only called if a wallet with a balance is found. Because that event is rare, this function is not significant 
    to the main pipeline of the program and is not timed.
    """
    var = hashlib.sha256(binascii.unhexlify(hashlib.sha256(binascii.unhexlify('80' + private_key)).hexdigest())).hexdigest()
    var = binascii.unhexlify('80' + private_key + var[0:8])
    alphabet = chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    value = pad = 0; result = ''
    for i, c in enumerate(var[::-1]): value += 256**i * c
    while value >= len(alphabet):
        div, mod = divmod(value, len(alphabet))
        result, value = chars[mod] + result, div
    result = chars[value] + result
    for c in var:
        if c == 0: pad += 1
        else: break
    return chars[0] * pad + result
              
def main(database):
    """Create the main pipeline by using an infinite loop to repeatedly call the functions, while utilizing 
    multiprocessing from __main__. Because all the functions are relatively fast, it is better to combine
    them all into one process.
    """
    while True:
        private_key = generate_private_key()                # 0.0000061659 seconds
        public_key = private_key_to_public_key(private_key) # 0.0016401287 seconds
        address = public_key_to_address(public_key)         # 0.0000801390 seconds
        if address != -1:
            process(private_key, public_key, address, database) # 0.0000026941 seconds
                                                            # --------------------
                                                            # 0.0017291287 seconds
    
if __name__ == '__main__':
    """Read the pickle file.
    """
    infile = open(filename,'rb')
    database = pickle.load(infile)
    infile.close()
    # To verify the database size, remove the # from the line below
    #print('database size: ' + str(sum(len(i) for i in database))); quit()
    
    for cpu in range(multiprocessing.cpu_count()):
        multiprocessing.Process(target = main, args = (database, )).start()
   
