import copy

def is_numeric(value):
    try:
        float(value)
    except:
        return False
    return True


class SampleUnit(object):
    __value = None
    __rank = None

    def set_value(self, value):
        if is_numeric(value):
            self.__value = value
        else:
            raise Exception("Invalid value format")

    def set_rank(self, rank):
        if is_numeric(rank):
            self.__rank = rank
        else:
            raise Exception("Invalid rank format")

    def get_value(self):
        return self.__value

    def get_rank(self):
        return self.__rank

    def __init__(self, value, rank = 0):
        self.set_value(value)
        self.set_rank(rank)

    def __gt__(self, other):
        if is_sample_unit(other):
            return self.__value > other.__value
        raise Exception("Invalid type of other")

def is_numeric_list(data_list):
    for value in data_list:
        if not is_numeric(value):
            return False
    return True


def is_sample_unit(value):
    if type(value) is SampleUnit:
        return True
    return False

def is_sample_unit_list(data_list):
    for value in data_list:
        if not is_sample_unit(value):
            return False
    return True

class Sample(object):
    
    __data = None
    
    def update_data(self, data_list):
        if is_numeric_list(data_list):
            if len(data_list) < 3:
                raise Exception("Insufficient data!\nThe sample must contain at least 3 values")
            self.__data = []
            for value in data_list:
                self.__data.append(SampleUnit(value))
        elif is_sample_unit_list(data_list):
            self.__data = copy.deepcopy(data_list)
        else:
            raise Exception("Invalid data format")

    def get_data_list(self):
        return copy.deepcopy(self.__data)

    def __init__(self, numeric_list):
        self.update_data(numeric_list)


def is_sample(sample):
    if type(sample) is Sample:
        return True
    return False



class MannWhitneyUTest(object):
    __sample_one = None
    __sample_two = None

    __is_ready_for_work = False

    __sample_one_temp_data = None
    __sample_two_temp_data = None

    __merged_row = None

    __rank_sum_one = None
    __rank_sum_two = None

    __max_rank_sum = None
    __len_of_sample = None

    __empirical_u_test = None

    __critical_u_test = None

    __critical_value_table = [
        [   0,   1,   1,   2,   2,   3,   3,   4,   4,   5,   5,   6,   6,   7,   7,   8,   8,   9,   9,  10,  10,  11,  11,  12,  13,  13],

        [   1,   2,   3,   4,   4,   5,   6,   7,   8,   9,  10,  11,  11,  12,  13,  14,  15,  16,  17,  17,  18,  19,  20,  21,  22,  23],

        [   2,   3,   5,   6,   7,   8,   9,  11,  12,  13,  14,  15,  17,  18,  19,  20,  22,  23,  24,  25,  27,  28,  29,  30,  32,  33],

        [  -1,   5,   6,   8,  10,  11,  13,  14,  16,  17,  19,  21,  22,  24,  25,  27,  29,  30,  32,  33,  35,  37,  38,  40,  42,  43],

        [  -1,  -1,   8,  10,  12,  14,  16,  18,  20,  22,  24,  26,  28,  30,  32,  34,  36,  38,  40,  42,  44,  46,  48,  50,  52,  54],

        [  -1,  -1,  -1,  13,  15,  17,  19,  22,  24,  26,  29,  31,  34,  36,  38,  41,  43,  45,  48,  50,  53,  55,  57,  60,  62,  65],
        
        [  -1,  -1,  -1,  -1,  17,  20,  23,  26,  28,  31,  34,  37,  39,  42,  45,  48,  50,  53,  56,  59,  62,  64,  67,  70,  73,  76],

        [  -1,  -1,  -1,  -1,  -1,  23,  26,  29,  33,  36,  39,  42,  45,  48,  52,  55,  58,  61,  64,  67,  71,  74,  77,  80,  83,  87],

        [  -1,  -1,  -1,  -1,  -1,  -1,  30,  33,  37,  40,  44,  47,  51,  55,  58,  62,  65,  69,  73,  76,  80,  83,  87,  90,  94,  98],

        [  -1,  -1,  -1,  -1,  -1,  -1,  -1,  37,  41,  45,  49,  53,  57,  61,  65,  69,  73,  77,  81,  85,  89,  93,  97, 101, 105, 109],

        [  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  45,  50,  54,  59,  63,  67,  72,  76,  80,  85,  89,  94,  98, 102, 107, 111, 116, 120],

        [  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  55,  59,  64,  67,  74,  78,  83,  88,  93,  98, 102, 107, 112, 118, 122, 127, 131],

        [  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  64,  70,  75,  80,  85,  90,  96, 101, 106, 111, 117, 122, 125, 132, 138, 143],
        
        [  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  75,  81,  86,  92,  98, 103, 109, 115, 120, 126, 132, 138, 143, 149, 154],

        [  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  87,  93,  99, 105, 111, 117, 123, 129, 135, 141, 147, 154, 160, 166],
    
        [  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  99, 106, 112, 119, 125, 132, 138, 145, 151, 158, 164, 171, 177],
        
        [  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1, 113, 119, 126, 133, 140, 147, 154, 161, 168, 175, 182, 189],
        
        [  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1, 127, 134, 141, 149, 156, 163, 171, 178, 186, 193, 200],
        
        [  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1, 142, 150, 157, 165, 173, 181, 188, 196, 204, 212],
        
        [  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1, 158, 166, 174, 182, 191, 199, 207, 215, 223],
        
        [  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1, 175, 183, 192, 200, 209, 218, 226, 235],
        
        [  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1, 192, 201, 210, 219, 228, 238, 247],
        
        [  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1, 211, 220, 230, 239, 249, 258],
        
        [  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1, 230, 240, 250, 260, 270],
        
        [  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1, 250, 261, 271, 282],
        
        [  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1, 272, 282, 293],
        
        [  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1, 294, 305],
        
        [  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1,  -1, 317],
    ]

    __is_null_hypothesis_correct = None

    def is_ready_for_work(self):
        return self.__is_ready_for_work

    def update_samples(self, sample_one, sample_two):
        if is_sample(sample_one) and is_sample(sample_two):
            self.__sample_one = sample_one
            self.__sample_two = sample_two
            self.__is_ready_for_work = True
        else:
            raise Exception("Invalid sample format")

    def __update_and_sort_merged_row(self):
        self.__sample_one_temp_data = self.__sample_one.get_data_list()
        self.__sample_two_temp_data = self.__sample_two.get_data_list()
        
        self.__merged_row = []

        self.__merged_row.extend(self.__sample_one_temp_data)
        self.__merged_row.extend(self.__sample_two_temp_data)

        self.__merged_row.sort()

    def __assign_ranks_for_data_in_merged_row(self):
        next_rank = 1 
        
        for value in self.__merged_row:
            value.set_rank(next_rank)
            next_rank += 1;

        mutual_rank_counter = 0.0 
        prev_value = None
        same_rank_objects = []
            
        for unit in self.__merged_row:
            if prev_value == None:
                prev_value = unit.get_value()

            if prev_value == unit.get_value():
                same_rank_objects.append(unit)
                mutual_rank_counter += unit.get_rank()
            
            else:
                mutual_rank_counter /= len(same_rank_objects)
                for value in same_rank_objects:
                    value.set_rank(mutual_rank_counter)
                
                mutual_rank_counter = unit.get_rank()
                prev_value = unit.get_value()
                same_rank_objects = [unit]  
        
        if len(same_rank_objects) != 0:
            mutual_rank_counter /= len(same_rank_objects)
            for value in same_rank_objects:
                value.set_rank(mutual_rank_counter)
            same_rank_objects.clear()

    def __caluclate_rank_sums(self):
        self.__rank_sum_one = self.__rank_sum_two = 0.0
        for unit in self.__sample_one_temp_data:
            self.__rank_sum_one += unit.get_rank()
        for unit in self.__sample_two_temp_data:
            self.__rank_sum_two += unit.get_rank()


    def __define_max_rank_sum_and_len_of_sample(self):
        if self.__rank_sum_one > self.__rank_sum_two:
            self.__max_rank_sum = self.__rank_sum_one
            self.__len_of_sample = len(self.__sample_one_temp_data)
        else:
            self.__max_rank_sum = self.__rank_sum_two
            self.__len_of_sample = len(self.__sample_two_temp_data)

    def __define_empirical_u_test(self):
        self.__empirical_u_test = len(self.__sample_one_temp_data)*len(self.__sample_two_temp_data)
        self.__empirical_u_test += (self.__len_of_sample*(self.__len_of_sample + 1)) / 2
        self.__empirical_u_test -= self.__max_rank_sum

    def __define_critical_u_test(self):
        n1 = len(self.__sample_one_temp_data)
        n2 = len(self.__sample_two_temp_data)
        if n1 > n2:
            self.__critical_u_test = self.__critical_value_table[n2 - 3][n1 - 5]
        else:
            self.__critical_u_test = self.__critical_value_table[n1 - 3][n2 - 5]

    def __define_null_hypothesis_status(self):
        __is_null_hypothesis_correct = self.__empirical_u_test >= self.__critical_u_test

    def __init__(self):
        self.__is_ready_for_work = False

# Debugging block begins
samle_1_data = [
    102,
    105,
    109,
    90,
    130,
    117,
    117,
    125,
    134,
    109
] 

sample_2_data = [
    121,
    120,
    134,
    119,
    115,
    106,
    107,
    101,
    97,
    117
]



# Debugging block ends