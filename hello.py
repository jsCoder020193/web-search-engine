k = ['for','bat','good','lol']
for idx, j in enumerate(k[1:]):
    print(idx+1,j)


searchterm = ''
for x in k[0:-1]:
    searchterm += x + ' and '
searchterm+=k[-1]
print(":"+searchterm+":")