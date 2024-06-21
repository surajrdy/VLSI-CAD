from pcn import PCN_create
import sys

# Termination Cases
def DeMorgans(func, nvars, ncubes):
    complement = []
    counter = 0
    for y in range(ncubes):
        for x in range(nvars):
            if func[y][x] == '11':
                counter += 1
    # All don't care Cube
    if counter == nvars:
        complement = [['']]
        return complement
    for y in range(ncubes):
        for x in range(nvars):
            if func[y][x] == "01":
                new_cube = ['11'] * nvars
                new_cube[x] = "10"
                complement.append(new_cube)
            elif func[y][x] == "10":
                new_cube = ['11'] * nvars
                new_cube[x] = "01"
                complement.append(new_cube)
    return complement

def Final(func, nvars, ncubes):
    print(func)
    if len(func) == 0:
        return [['11'] * nvars]
    elif len(func) == 1:
        return DeMorgans(func, nvars, ncubes)
    else:
        for x in range(ncubes):
            if func[x] == ['11' * nvars]:
                return [['']]
        # Code bulk of project
        z = BinateSelection(func, nvars, ncubes)
        print(z)
        P = CoFactor(func, z, 'true', ncubes)
        N = CoFactor(func, z, 'neg', ncubes)
        P_n = Final(P, nvars, len(P))
        N_n = Final(N, nvars, len(N))
        P_c = AND(P_n, z, 'true')
        N_c = AND(N_n, z, 'comp')
        answer = OR(P_c, N_c)
        return answer

def BinateVariable(function, nvars, ncubes):
    true_count = [0] * nvars
    neg_count = [0] * nvars

    binate_list = [False] * nvars
    binate = False

    for x in range(ncubes):
        for y in range(nvars):
            if function[x][y] == '01':
                true_count[y] += 1
            elif function[x][y] == '10':
                neg_count[y] += 1
    
    for y in range(nvars):
        if true_count[y] > 0 and neg_count[y] > 0:
            binate_list[y] = True
            binate = True

    return true_count, neg_count, binate_list, binate

def BinateSelection(function, nvars, ncubes):
    true_count, neg_count, binate_list, binate = BinateVariable(function, nvars, ncubes)
    if binate:
        final_binate = None
        most_binate = 0
        tiebreaker = False
        for y in range(nvars):
            if binate_list[y]:
                b_counter = true_count[y] + neg_count[y]
                if b_counter > most_binate:
                    most_binate = b_counter
                    final_binate = y
                    tiebreaker = False
                elif b_counter == most_binate:
                    tiebreaker = True
        if tiebreaker:
            TC = [abs(true_count[y] - neg_count[y]) if binate_list[y] else float('inf') for y in range(nvars)]
            min_TC = min(TC)
            final_binate = TC.index(min_TC)
        return final_binate
    else:
        max_unate = 0
        winner = None
        for y in range(nvars):
            if true_count[y] > max_unate or neg_count[y] > max_unate:
                max_unate = max(true_count[y], neg_count[y])
                winner = y
        return winner

def OR(cofunction1, cofunction2):
    combined_function = []
    for i in cofunction1:
        combined_function.append(i)
    for j in cofunction2:
        combined_function.append(j)
    return combined_function

def AND(cofunction, mostbinate, factor):
    for i in range(len(cofunction)):
        if factor == 'comp':
            cofunction[i][mostbinate] = '10'
        elif factor == 'true':
            cofunction[i][mostbinate] = '01'
    return cofunction

def CoFactor(function, mostbinate, term, ncubes):
    cofactor = []
    terminator = '10' if term == 'true' else '01' 
    opposite = '01' if term == 'true' else '10'
    
    for i in range(ncubes):
        if function[i][mostbinate] != terminator:
            new_cube = function[i].copy()
            if function[i][mostbinate] == opposite:
                new_cube[mostbinate] = '11' 
            cofactor.append(new_cube)
    return cofactor

def format_answer(answer):
    output = []
    for cube in answer:
        formatted_cube = ""
        for idx, val in enumerate(cube):
            if val == '01':
                formatted_cube += f"{idx+1}"
            elif val == '10':
                formatted_cube += f"-{idx+1}"
        output.append(formatted_cube)
    return output

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <filename>")
        return

    filename = sys.argv[1]
    with open(filename, 'r') as file:
        file_content = file.read()

    pcn_list, nvars, ncubes = PCN_create(file_content)
    output = Final(pcn_list, nvars, ncubes)
    ans = format_answer(output)
    for line in ans:
        print(line)

if __name__ == "__main__":
    main()