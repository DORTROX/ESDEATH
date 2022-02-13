summ = 0
a = 'Sum of 5 and 10'
a = a[7:]
a = a.split('and ')
for i in a:
    i = int(i)
    summ += a
print(summ)