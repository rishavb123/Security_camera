def encode(s):
    temp = ''
    for x in range(len(s)):
        temp+=chr(ord(s[len(s)-1-x])+5)
    temp2 = ''
    for x in range(0,len(temp),2):
        temp2+=temp[x]
    for x in range(1,len(temp),2):
        temp2+=temp[x]
    return temp2

def decode(s):
    temp = ''
    temp2 = ''
    for x in range(len(s)):
        if x<len(s)/2:
            temp+=s[x]
        else:
            temp2+=s[x]
    temp3 = ''
    for x in range(len(s)):
        if x%2==0:
            temp3+=temp[x/2]
        else:
            temp3+=temp2[x/2]
    temp4 = ''
    for x in range(len(temp3)):
        temp4+=chr(ord(temp3[len(temp3)-1-x])-5)
    return temp4
