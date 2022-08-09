str ='yaniv co'
arry = [[1,2,3],[2,3,4]]

def sum(arry):
    sum = 0
    for inner in arry:
        for j in inner:
            sum += j
    return sum

# print(sum(arry))

def rev(srt: str):
    out = ''
    for ch in srt:
        out = ch + out
    return out

# def rev(srt: str):
#     out = ''
#     for i in range(len(srt)):
#         out += str[len(srt)-1-i]
#     return out

print(rev(str))