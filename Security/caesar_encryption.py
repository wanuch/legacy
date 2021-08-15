def caesar_substitution_cipher():
    
    key = 3
    ciphertext = ''
    plaintext = input('Please enter the message: ')
    
    for i in plaintext:
        if i.isalpha():
            num = ord(i)
            num += key

            if i.isupper():
                if num > ord('Z'):
                     num -= 26
            elif i.islower():
                if   num > ord('z'):
                     num -= 26
               
            ciphertext += chr(num)
        else:
            ciphertext += i
            
    print (ciphertext) # For checking the ciphertext
    return ciphertext
    
caesar_substitution_cipher()