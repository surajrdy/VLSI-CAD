from pcn import PCN_create
import sys
from typing import List, Tuple

TRUE = '01'
FALSE = '10'
DC = '11'

''' 
DeMorgans function takes in the single cube function and the number of variables and cubes and returns the complement
'''
def DeMorgans(func, nvars, ncubes):
    complement = []
    #Counter variable intitialized for don't care cubes that will invoke a new cube
    dc_counter = 0
    for y in range(ncubes):
        for x in range(nvars):
            if func[y][x] == DC:
                dc_counter += 1
    # Edge case for All don't care Cube meaning complement would be an empty list since complement of 1 = 0
    if dc_counter == nvars:
        complement = [['']]
        return complement
    #Iterate through PCN list and implement DeMorgans
    for y in range(ncubes):
        for x in range(nvars):
            if func[y][x] == FALSE:
                new_cube = [DC] * nvars
                new_cube[x] = TRUE
                complement.append(new_cube)
            elif func[y][x] == TRUE:
                new_cube = [DC] * nvars
                new_cube[x] = FALSE
                complement.append(new_cube)
    return complement

#Final function represents the full functionality of the complement functions and returns the PCN list answer for the complement
def Final(func, nvars, ncubes):
    '''
    Termination cases
    '''
    #Empty Cube List
    if len(func) == 0:
        return [[DC] * nvars]
    #Cube list contains just one cube
    elif len(func) == 1:
        return DeMorgans(func, nvars, ncubes)
    else:
        #Cube list contains all Don't Cares Cube, meaning entire function is 1
        for c in func:
            if all(val == DC for val in c):
                return [['']]
        #Recursive steps as outlined by algorithm in Project Instructions which follows Shannons Complement Function
        z = BinateSelection(func, nvars, ncubes)
        P = CoFactor(func, z, 'true', ncubes)
        N = CoFactor(func, z, 'neg', ncubes)
        P_c = AND(Final(P, nvars, len(P)), z, 'true')
        N_c = AND(Final(N, nvars, len(N)), z, 'comp')
        #No need for OR function as '+' executes same process
        answer = P_c + N_c
        return answer

'''
BinateVariable gives foundational information for selecting the most binate variable by providing:
1. List of variables and the appearances of 'true' and 'false' in each cube
2. Whether each variable is binate or not
3. Whether the function contains any binate variables or not
'''
def BinateVariable(function, nvars, ncubes):
    true_count = [0] * nvars
    neg_count = [0] * nvars
    binate_list = [False] * nvars
    binate = False

    for x in range(ncubes):
        for y in range(nvars):
            if function[x][y] == TRUE:
                true_count[y] += 1
            elif function[x][y] == FALSE:
                neg_count[y] += 1
    
    for y in range(nvars):
        if true_count[y] > 0 and neg_count[y] > 0:
            binate_list[y] = True
            binate = True
    return true_count, neg_count, binate_list, binate

'''
BinateSelection selects the most binate variable using information from the BinateVariable function
    1. If there is a tie, it selects the variable with the smallest difference between true and negative counts: |T-C|
    2. If there is still a tie, it selects the variable with the smallest index
    3. If the function is unate, it selects the variable with the most appearances of 'true' or 'false'
    4. If there exists a tie with this process as well, it selects the variable with the smallest index
'''
def BinateSelection(function, nvars, ncubes):
    true_count, neg_count, binate_list, binate = BinateVariable(function, nvars, ncubes)
    if binate:
        #final_binate represents the index that the most binate variable exists
        final_binate = None
        #most_binate variable represents the flexible variable for the binate variable as the for loop continues
        most_binate = 0
        tiebreaker = False
        #For loop for indentifying initial condition for most_binate if the variable appears the most times
        for y in range(nvars):
            if binate_list[y]:
                b_counter = true_count[y] + neg_count[y]
                if b_counter > most_binate:
                    most_binate = b_counter
                    final_binate = y
                    tiebreaker = False
                elif b_counter == most_binate:
                    tiebreaker = True
        if tiebreaker == True:
            #Initialize list for true_count with -1 to take care of unate variables which will have the minimum
            TC = [-1] * nvars
            #Initialized variable that sets the first |T-C| value for comparison
            min = true_count[0] - neg_count[0]
            winner = None
            #Intalize variable for second tiebreaker concerning the smallest index
            lowest_index_count = 0
            #For loop sets up respective |T-C| count for each variable index and ignores unate variables
            for y in range(nvars):
                if binate_list[y] == True:
                    TC[y] = abs(true_count[y] - neg_count[y])
            #For loop to iterate through function to indentify the smallest |T-C| count
            for y in range(nvars):
                if min > TC[y] and TC[y] != -1:
                    min = TC[y]
                    winner = y
                elif min == TC[y]:
                    lowest_index_count+=1
            #Acts as a second tiebreaker variable and iterates through list to find which index corresponds to minimum value
            if lowest_index_count > 1:
                for y in range(nvars):
                    if TC[y] == min:
                        final_binate = y
                        break
            #Erases need for second hand tiebreaker
            elif lowest_index_count <= 1:
                final_binate = winner
            return final_binate
        return final_binate
    #If function is unate, go through most-appearance process for function
    else:
        max_unate = 0
        winner = None
        for y in range(nvars):
            if true_count[y] > max_unate or neg_count[y] > max_unate:
                max_unate = max(true_count[y], neg_count[y])
                winner = y
        return winner

#AND Function representing Boolean Algebra operation
def AND(cofunction, mostbinate, factor):
    for c in cofunction:
        #Edge case for empty cube list
        if c != ['']:
            if factor == 'comp':
                c[mostbinate] = FALSE
            elif factor == 'true':
                c[mostbinate] = TRUE
    return cofunction

'''
Combined function for Shannon CoFactor expansion
    1. Takes in the function, the most binate variable, and the term of 'true' or 'compl' to be used in the expansion 
    2. Returns the cofactor of the function with respect to the most binate variable
'''
def CoFactor(function, mostbinate, term, ncubes):
    cofactor = []
    #Terminator variable initialized for ignoring cube
    terminator = FALSE if term == 'true' else TRUE 
    #Opposite variable intialized for complementing the 01 or 10 indexed variable
    opposite = TRUE if term == 'true' else FALSE
    
    for i in range(ncubes):
        if function[i][mostbinate] != terminator:
            #Create a new cube and go through mechanics of Cofactor Expansion
            new_cube = function[i].copy()
            if function[i][mostbinate] == opposite:
                new_cube[mostbinate] = DC 
            cofactor.append(new_cube)
    return cofactor

'''
Subset and Redundancy functions are used to format the output answer to optimize the solution
'''
def Subset(cube1, cube2):
    # Check each pair of corresponding elements from cube1 and cube2
    for val1, val2 in zip(cube1, cube2):
        # If the elements are not equal and val1 is not a 'don't care' value, return False
        if val1 != val2 and val1 != DC:
            return False
    # If all pairs of elements match the condition, return True
    return True

def Redundancy(cubes):
    non_redundant = []
    # For loop to iterate over each cube in the list of cubes
    for c in cubes:
        # Check if the current cube is not a subset of any other cube
        is_redundant = False
        for other_cube in cubes:
            if c != other_cube and Subset(c, other_cube):
                is_redundant = True
                break
        
        # If the cube is not redundant, add it to the non_redundant list
        if not is_redundant:
            non_redundant.append(c)
    
    return non_redundant

'''
Formatting the PCN list back to the original input file format is important and the format_answer function completes this.
'''
def format_answer(answer):
    seen_cubes = set()
    output = []

    answer = Redundancy(answer)

    for c in answer:
        #Eliminates printing of empty cube lists
        if c != ['']:
            formatted = []
            for idx, val in enumerate(c):
                #Positive variable instances
                if val == TRUE:
                    formatted.append(str(idx + 1)) 
                #Negative variable instances
                elif val == FALSE:
                    formatted.append(f'-{idx + 1}')
            text = ' '.join(formatted)
            #Adding variable count to start of each line
            if text not in seen_cubes:
                output.append(f"{len(text)} {text}")
                seen_cubes.add(text)
    
    return output

def main():
    filename = sys.argv[1]
    with open(filename, 'r') as file:
        file_content = file.read()

    pcn_list, nvars, ncubes = PCN_create(file_content)
    output = Final(pcn_list, nvars, ncubes)
    ans = format_answer(output)
    output_filename = "output.txt"

    with open(output_filename, "w") as fh:
        fh.write(f"{nvars}\n")
        fh.write(f"{len(ans)}\n")
        for line in ans:
            fh.write(line + "\n")
    
    print(f"Output: {output_filename}")

if __name__ == "__main__":
    main()