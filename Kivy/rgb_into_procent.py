rgb_Value =[149, 0, 255]
result =[]
amb = ''
for i in rgb_Value:
    x = i/255
    result.append(round(x,2))
for i in result:
    amb = amb + str(i) +', '
amb = amb + '1'
print(amb)