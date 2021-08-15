def one_time_pad():
    
    key = 0
    count = 0
    ciphertext = ''
    plaintext = input('Please enter the message: ')
    key_text = 'thequickbrownfoxjumpsoverthelazydog'
    
    for i in plaintext:
      
        if i.isalpha():
            num = ord(i)
            
            if count >= len(key_text):
                key = 0
            else:
                key = ord(key_text[count]) - 97
            
            num += key

            if i.isupper():
                if num > ord('Z'):
                     num -= 26
            elif i.islower():
                if   num > ord('z'):
                     num -= 26
               
            ciphertext += chr(num)
            count +=1
        else:
            ciphertext += i
    
    print (ciphertext) # For checking the ciphertext
    return ciphertext
    
one_time_pad()