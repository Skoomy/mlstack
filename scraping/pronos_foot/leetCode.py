import itertools


if __name__ == '__main__':

    vector = [2,7,11,15]
    target = 9
    res = itertools.combinations(vector,2)

    for each in res:
       # print(each)
        if sum(each) == target:
            print(each)
            get_indexes = lambda x, vector: [i for (each, i) in zip (vector, range (len (vector))) if x == target]
            print(vector.index(each[0]))
            print (vector.index (each[1]))

