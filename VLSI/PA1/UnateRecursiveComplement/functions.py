from pcn import PCN_create
from io import StringIO
import sys

answer = None


#Termination Cases
def DeMorgans(func, nvars):
    #Check for new cube list size
    complement = [[['11'] * nvars] * non_dc]
    non_dc = nvars
    counter = 0
    for x in range(nvars):
        if func[0][x] == '11':
            non_dc - 1
            counter+=1
    #All don't care Cube
    if counter == nvars:
        complement = [['']]
    c = 0
    for x in range(nvars):
        if func[0][x] == "01":
            complement[c][x] == "10"
            c += 1
        elif func[0][x] == "10":
            complement[c][x] == "01"
            c += 1
        else: 
            c+1
    return complement

def Final(func, nvars, ncubes):
    if len(func) == 0:
        return [['11'] * nvars]
    elif len(func) == 1:
        return DeMorgans(func, nvars)    
    else:
        counterDC = 0
        for x in range(ncubes):
            for y in range(0, nvars):
                if func[x] == [['11' * nvars]]:
                    return [['']]
        #Code bulk of project
        z = BinateSelection(func, nvars, ncubes)
        P = CoFactor(func, z, 'true', ncubes)
        N = CoFactor(func, z, 'neg', ncubes)
        P_n = Final(P, nvars)
        N_n = Final(N, nvars)
        P_c = AND(z, P_n, 'true')
        N_c = AND(z, N_n, 'comp')
        answer = OR(P_c, N_c)
        return answer
    return answer

def BinateVariable(function, nvars, ncubes):

    cubes = function

    true_count = [0] * nvars
    neg_count = [0] * nvars
    binate_list = [False] *nvars
    binate = False

    for x in range(ncubes):
        for y in range(0, nvars-1):
            if cubes[x][y] == '01':
                true_count[y] += 1
            elif cubes[x][y] == '10':
                neg_count[y] += 1
    
    for y in range(nvars):
        if true_count[y] > 0 and neg_count > 0:
            binate_list[y] = True
            binate = True

    return true_count, neg_count, binate_list, binate

def BinateSelection(function, nvars, ncubes):

    true_count, neg_count, binate_list, binate = BinateVariable(function, nvars, ncubes)

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
        for y in range(nvars):
            if true_count[y] or neg_count[y] > max_unate:
                max_unate = max(true_count[y], neg_count[y])
                winner = y
            else:
                for x in range(nvars):
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
            cofunction[i][mostbinate-1] = '10'
        elif factor =='true':
            cofunction[i][mostbinate-1] = '01'
    return cofunction

    
    return
def CoFactor(function, mostbinate, term, ncubes):
    cofactor = []
    terminator = None
    opposite = None
    cube_count = 0
    if term == 'true':
        terminate = '10'
        opposite = '01'
    else:
        terminate = '01'
        opposite = '10'
    for i in range(ncubes):
        if function[i][mostbinate-1] != terminator:
            cube_count += 1
            new_cube = function[i][:]
            for j in range(len(function[i])):
                new_cube[cube_count][j] = function[i][j]
                if j == mostbinate-1:
                    if function[i][j] == opposite:
                        new_cube[cube_count][j] = '11'
            cofactor.append(new_cube)
    return cofactor

def format(answer):
    output = [0]
    for x in answer:
        counter = 0
        for y in answer[x]:
            if y != '11':
                counter += 1
                if y == '01':
                    output[x][counter] == str(y)
                elif y =='10':
                    output[x][counter] == '-' + str(y)
    return output


def main():
    if len(sys.argv) != 2:
        print("Usage: python pcn_reader.py <filename>")
        return

    filename = sys.argv[1]
    with open(filename, 'r') as file:
            file_content = file.read()

    pcn_list, nvars, ncubes = PCN_create(file_content)
    output = Final(pcn_list, nvars, ncubes)
    ans = format(output)
    print(ans)
    if __name__ == "__main__":
        main()