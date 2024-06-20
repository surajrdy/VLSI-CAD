from pcn import PCN_create
from io import StringIO
import sys



filename = sys.argv[1]
with open(filename, 'r') as file:
    file_content = file.read()

pcn_list, nvars, ncubes = PCN_create(file_content)


#Termination Cases
def DeMorgans(pcn, nvars, ncubes):
    #Check for new cube list size
    complement = [[['11'] * nvars] * non_dc]
    non_dc = nvars
    counter = 0
    for x in range(0, nvars-1):
        if pcn[0][x] == '11':
            non_dc - 1
            counter+=1
    #All don't care Cube
    if counter == nvars:
        complement = [['']]
    c = 0
    for x in range(0, nvars-1):
        if pcn[0][x] == "01":
            complement[c][x] == "10"
            c += 1
        elif pcn[0][x] == "10":
            complement[c][x] == "01"
            c += 1
        else: 
            c+1
    return complement

def Complement(pcn, nvars, ncubes):
    if len(pcn) == 0:
        return [['11'] * nvars]
    elif len(pcn) == 1:
        return DeMorgans(pcn, nvars, ncubes)    
    else:
        counterDC = 0
        for x in range(0, ncubes-1):
            for y in range(0, nvars):
                if pcn[x] == [['11' * nvars]]:
                    return [['']]
        #Code bulk of project
        z = BinateSelection(pcn, nvars, ncubes)

        return answer
    return answer

def BinateVariable(function, nvars, ncubes):

    cubes = function

    true_count = [0] * nvars
    neg_count = [0] * nvars
    binate_list = [False] *nvars
    binate = False

    for x in range(0, ncubes):
        for y in range(0, nvars-1):
            if cubes[x][y] == '01':
                true_count[y] += 1
            elif cubes[x][y] == '10':
                neg_count[y] += 1
    
    for y in range(0, nvars-1):
        if true_count[y] > 0 and neg_count > 0:
            binate_list[y] = True
            binate = True

    return true_count, neg_count, binate_list, binate

def BinateSelection(pcn, nvars, ncubes):

    true_count, neg_count, binate_list, binate = BinateVariable(pcn, nvars, ncubes)

    if binate == True:
        final_binate = None
        most_binate = 0
        tiebreaker = False
        for y in range(0, nvars-1):
            if binate_list[y] == True:
                b_counter = true_count[y] + neg_count[y] 
                if b_counter > most_binate:
                    most_binate = b_counter
                    final_binate = y
                    tiebreaker = False
                elif b_counter == most_binate:
                    tiebreaker = True
        if tiebreaker == True:
            TC = [-1] * nvars
            min = true_count[0] - neg_count[0]
            winner = None
            lowest_index_count = 0
            for y in range(0, nvars-1):
                if binate_list[y] == True:
                    TC[y] = abs(true_count[y] - neg_count[y])
            for y in range(0, nvars-1):
                if min > TC[y] and TC[y] != -1:
                    min = TC[y]
                    winner = y
                elif min == TC[y]:
                    lowest_index_count+=1
            if lowest_index_count > 1:
                for y in range(0, nvars-1):
                    if TC[y] == min:
                        final_binate = y
                        break
            elif lowest_index_count <= 1:
                final_binate = winner
            return final_binate
        else:
            return final_binate
    #Unate Function
    else:
        max_unate = 0
        winner = None
        for y in range(0, nvars-1):
            if true_count[y] or neg_count[y] > max_unate:
                max_unate = max(true_count[y], neg_count[y])
                winner = y
            else:
                for x in range(0, nvars-1):
                    if true_count[x] or neg_count[x] == max_unate:
                        winner = x
        return winner

def OR(cofunction1, cofunction2):
    combined_function = []
    for i in cofunction1:
        combined_function.append(i)
    for j in cofunction2:
        combined_function.append(i)
    return combined_function

def AND(cofunction, mostbinate, factor):
    for i in range(len(cofunction)):
        if factor == 'comp':
            cofunction[i][mostbinate] = '10'
        elif factor =='true':
            cofunction[i][mostbinate] = '01'
    return cofunction

    
    return
def CoFactor(function, mostbinate, term):
    cofactor = []

    for i in range(ncubes-1):
        
    return
