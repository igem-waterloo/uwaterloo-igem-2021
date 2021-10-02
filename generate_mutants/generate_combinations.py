from itertools import combinations

def all_double_mutants(single_list): 
    # Get all pairs in List
    # Using combinations()
    res = list(combinations(single_list, 2))

    with open('doubleMutants_duplicated.txt', 'a') as end_file:
        end_file.truncate() 
        for i in range(0, len(res)):
            end_file.write(res[i][0])
            end_file.write(" ")
            end_file.write(res[i][1])
            end_file.write("\n")

    with open('doubleMutants_duplicated.txt') as double_file:
        double_list = [line.rstrip() for line in double_file]

    with open('doubleMutants.txt', 'a') as result_file:
        result_file.truncate() 
        for line in double_list:
            if line[2:5] != line[10:13]:
                result_file.write(line)
                result_file.write("\n")


def more_than_two_mutants(single_list, res_num): 
    # Get all pairs in List
    # Using combinations()
    res = []
    for i in range(3, res_num+1):
        res = res + list(combinations(single_list, i))
    print(str(res))

    with open('multiMutants_duplicated.txt', 'a') as end_file:
        end_file.truncate() 
        for i in range(0, len(res)):
            for j in range(0, len(res[i])):
                end_file.write(res[i][j])
                if j == len(res[i])-1:
                    end_file.write("\n")
                else: 
                    end_file.write(" ")

    with open('multiMutants_duplicated.txt') as end_file:
        multi_list = [line.rstrip() for line in end_file]

    with open('multiMutants.txt', 'a') as result_file:
        result_file.truncate() 
        for line in multi_list:
            if len(line) <= 24: 
                if line[2:5] != line[10:13] and line[2:5] != line[18:21] and line[10:13] != line[18:21]:
                    result_file.write(line)
                    result_file.write("\n")
            elif len(line) > 24: 
                if line[2:5] != line[10:13] and line[2:5] != line[18:21] and line[2:5] != line[26:29] and line[10:13] != line[18:21] and line[10:13] != line[26:29] and line[18:21] != line[26:29]:
                    result_file.write(line)
                    result_file.write("\n")
            
# initializing single mutant list 
with open('single_mutants.txt') as f:
    single_list = [line.rstrip() for line in f]
  
# printing original list in console
print("The original list : " + str(single_list))

all_double_mutants(single_list)
      
more_than_two_mutants(single_list, 4)
