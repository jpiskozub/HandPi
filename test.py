import numpy as np
import csv
from time import gmtime, strftime


input = np.random.randint(20000,25000,[1000,10])
sign = 'a'
#charar = sign*1000
charar = np.array(['b' for i in range(1000)],dtype='str')
#charar[:] = sign
result=np.c_[input,charar]

with open("test.csv", mode='w', encoding='utf-8') as file:
            writer = csv.writer(file,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
            writer.writerow([])
            np.savetxt(file,result, delimiter = ',',fmt='%s' )
            