# Модуль MannWhitney (без сторонних библиотек)
#  - определяет эмпирическое значение U-критерия для двух заданных выборок
#  - определяет критичекое значение U-критерия для двух заданных выборок
#  - проверяет истинновсть нулевой гипотезы

# Автор: Цветков В.О.

def is_numeric(value):
    try:
        float(value)
    except:
        return False
    return True

def is_numeric_list(data_list):
    if type(data_list) is list:
        for data_list_unit in data_list:
            if not is_numeric(data_list_unit):
                return False
        return True
    else:
        raise Exception("The \"data_list\" must be a list.\nBut now it is \"{}\".".format(type(data_list)))

class RankedNumber(object):
    __number = None
    __rank = None
    
    # Mutators

    def set_number(self, number):
        if is_numeric(number):
            self.__number = number
        else:
            raise Exception("{}:\n\tThe argument \"number\" must be a number.\nBut now it is \"{}\".".format(self, type(number)))

    def set_rank(self, rank):
        if is_numeric(rank):
            self.__rank = rank
        else:
            raise Exception("{}:\n\tThe argument \"rank\" must be a number.\nBut now it is \"{}\".".format(self, type(rank)))

    # Accessers

    def get_number(self):
        return self.__number

    def get_rank(self):
        return self.__rank

    # Constructor

    def __init__(self, number, rank = 0):
       self.set_number(number)
       self.set_rank(rank)

    # Other instructions
    
    def __gt__(self, other):
        if is_ranked_number(other):
            return self.__number > other.__number
        raise Exception("{}:\n\tThe argument \"other\" must be a RankedNumber.\nBut now it is \"{}\".".format(self, type(other)))


def is_ranked_number(value):
    if type(value) is RankedNumber:
        return True
    return False

# Данный класс объединяет в себе данные из двух списков,
# включающих в себя 3-30 и 5-30 числовых (вещественных или целых, со знаком или без) значений соответственно.
# Необходим чтобы задать ограничения на входные данные
class SampleBlock(object):
    __samples_data_list = None

    # Mutator

    def set_samples_data_list(self, sample_one_data, sample_two_data):
        if not is_numeric_list(sample_one_data):
            raise Exception("{}:\n\tThe \"sample_one_data\" must be a list of numbers.\nBut not a number was found.".format(self))
        if not is_numeric_list(sample_two_data):
            raise Exception("{}:\n\tThe \"sample_two_data\" must be a list of numbers.\nBut not a number was found.".format(self))
        if (
            len(sample_one_data) < 3 and len(sample_two_data) < 5 or
            len(sample_one_data) < 5 and len(sample_two_data) < 3
         ):
            raise Exception("{}:\n\tThe sample sizes are too small.\nOne of the samples must contain at least three values,\nand the second must contain at least five.".format(self))

        if (
            len(sample_one_data) > 30 or len(sample_two_data) > 30
        ):
            raise Exception("{}:\n\tThe sample sizes are too large.\nA sample must contain no more then thirty values.".format(self))

        self.__samples_data_list = []
        self.__samples_data_list.append(sample_one_data)
        self.__samples_data_list.append(sample_two_data)


    # Accesser

    def get_samples_data_list(self):
        return list(self.__samples_data_list)

    # Constructor

    def __init__(self, sample_one_data, sample_two_data):
       self.set_samples_data_list(sample_one_data, sample_two_data)


def is_sample_block(value):
    if type(value) is SampleBlock:
        return True
    return False

def generate_ranked_list_from_numeric_list(numeric_list):
    if is_numeric_list(numeric_list):
        ranked_list = []
        for numeric_list_unit in numeric_list:
            ranked_list.append(RankedNumber(numeric_list_unit))
        return ranked_list
    else:
        raise Exception("The \"numeric_list\" must be a list of numbers.\nBut not a number was found.")


class MannWhitney(object):

    # Private data
    
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

    __is_ready_for_work = None

    __sample_block = None
    __ranked_sample_data_list = None
    __merged_ranked_list = None
    __rank_sum_list = None
    __max_rank_sum_index = None
    __empirical_u_test = None

    # Mutator

    def set_sample_block(self, sample_block):
        if is_sample_block(sample_block):
            self.__sample_block = sample_block
        else:
            raise Exception("{}:\n\tThe \"sample_block\" must be SampleBlock".format(self))

    # Private methods

    def __generate_sample_ranked_block(self):
        self.__ranked_sample_data_list = []
        for sample_data in self.__sample_block.get_samples_data_list():
            self.__ranked_sample_data_list.append(
                generate_ranked_list_from_numeric_list(
                    sample_data
                )
            )    

    def __generate_merged_ranked_list(self):
        self.__merged_ranked_list = []
        for ranked_sample_data in self.__ranked_sample_data_list:
            self.__merged_ranked_list.extend(ranked_sample_data)

    def __assign_ranks_for_merged_ranked_list(self):
        self.__merged_ranked_list.sort(reverse = True)
        next_rank = 1 
        
        for value in self.__merged_ranked_list:
            value.set_rank(next_rank)
            next_rank += 1;

        mutual_rank_counter = 0.0 
        prev_number = None
        same_rank_objects = []
            
        for merged_ranked_list_unit in self.__merged_ranked_list:
            if prev_number == None:
                prev_number = merged_ranked_list_unit.get_number()

            if prev_number == merged_ranked_list_unit.get_number():
                same_rank_objects.append(merged_ranked_list_unit)
                mutual_rank_counter += merged_ranked_list_unit.get_rank()
            
            else:
                mutual_rank_counter /= len(same_rank_objects)
                for same_rank_objects_unit in same_rank_objects:
                    same_rank_objects_unit.set_rank(mutual_rank_counter)
                
                mutual_rank_counter = merged_ranked_list_unit.get_rank()
                prev_number = merged_ranked_list_unit.get_number()
                same_rank_objects = [merged_ranked_list_unit]  
        
        if len(same_rank_objects) != 0:
            mutual_rank_counter /= len(same_rank_objects)
            for same_rank_objects_unit in same_rank_objects:
                same_rank_objects_unit.set_rank(mutual_rank_counter)
            same_rank_objects.clear()

    def __caluclate_rank_sums(self):
        self.__rank_sum_list = []
        self.__rank_sum_list.append(0)
        self.__rank_sum_list.append(0)
        for i in range(2):
            for ranked_sample_data_list_unit in self.__ranked_sample_data_list[i]:
                self.__rank_sum_list[i] += ranked_sample_data_list_unit.get_rank();

    def __define_max_rank_sum_index(self):
        if self.__rank_sum_list[0] > self.__rank_sum_list[1]:
            self.__max_rank_sum_index = 0
        else:
            self.__max_rank_sum_index = 1

    def __define_empirical_u_test(self):
        self.__empirical_u_test = len(self.__ranked_sample_data_list[0]) * len(self.__ranked_sample_data_list[0])
        self.__empirical_u_test += (len(self.__ranked_sample_data_list[self.__max_rank_sum_index])*(len(self.__ranked_sample_data_list[self.__max_rank_sum_index]) + 1))/2
        self.__empirical_u_test -= self.__rank_sum_list[self.__max_rank_sum_index]


    # Public methods

    def calculate_empirical_u_test(self):
        self.__generate_sample_ranked_block()
        self.__generate_merged_ranked_list()
        self.__assign_ranks_for_merged_ranked_list()
        self.__caluclate_rank_sums()
        self.__define_max_rank_sum_index()
        self.__define_empirical_u_test()
        return self.__empirical_u_test

    def get_critical_u_test(self):
        return self.__critical_value_table[len(self.__ranked_sample_data_list[1 - self.__max_rank_sum_index]) - 3][len(self.__ranked_sample_data_list[self.__max_rank_sum_index]) - 5]

    def is_null_hypothesis_correct(self):
        return self.__empirical_u_test >= self.get_critical_u_test()

    # Constructor

    def __init__(self):
        self.__is_ready_for_work = False
