#PCN Functions
from io import StringIO
import sys

#Reading in array and converting to pcn list
def PCN_create( file ):
    #Read and split array by lines
    inter = Convert(file)
    nvars = inter[0][0]
    ncubes = inter[1][0]

    #Now we will create the actual PCN list with 10 = complement, 01 = true, and 11 = DC. It is optimal to populate everything with DC first, and then add the variables when they are true/complement

    #Fill pcn_list with 11 for DC and use for _ for junk variable
    pcn_list = [['11'] * nvars for _ in range(ncubes)]
    for i in range(2, len(inter)):
        for j in range(1, len(inter[i])):
            #Variable being parsed through
            var = inter[i][j]
            #For True variables
            if var > 0:
                pc = '01'
            #For complement variables
            elif var < 0:
                pc = '10'
            #Define the PCN notation now
            pcn_list[i-2][abs(var)-1] = pc

    return pcn_list, nvars, ncubes

def Convert(file):
    initial = StringIO(file)
    array = [list(map(int, x.split())) for x in initial.read().splitlines() if x.strip()]
    return array
