NAME = 0
INFO = 1
RATING = 0
COUNTRY = 1
CLUB = 2

FIRST_LETTER = 0


class Dictionary(object):

    data_dict = dict()


    def __init__(self, filename):
        self.load_csv(filename)
    

    def load_csv(self, filename):
        # CSV file must have in first column Key
        # Other columns will become Value as list

        file = open(filename, "r")

        data = []

        for line in file.readlines():
            tmp = line.split(",")
            tmp[len(tmp) - 1] = tmp[len(tmp) - 1][:-1] # delete \n at the end of last field
            data.append(tmp)

        file.close()

        parsed_data = []

        for record in data: # delete not unique name
            if record[NAME] not in [result[NAME] for result in parsed_data]:
                parsed_data.append(record)

        for i in range(len(parsed_data)):
            key = parsed_data[i][NAME]
            value = [parsed_data[i][ind] for ind in range(1, len(parsed_data[i]))]

            self.data_dict[key] = value


    def print_record(self, record): # For footballers only
        print("Name: %s\nRating: %s, Country: %s, Club: %s\n" \
                    %(record[NAME], record[INFO][RATING], record[INFO][COUNTRY], record[INFO][CLUB]))


    def print_dict(self):
        if (len(self.data_dict) == 0):
            print("\nОшибка: Словарь пуст\n")
            return

        all_records = self.data_dict.items()

        for record in all_records:
            self.print_record(record)


    def full_search(self, key, output = True):
        count = 0 # count of comparsions

        keys = self.data_dict.keys()

        for elem in keys:
            count += 1

            if (elem == key):
                if (output):
                    record = [key, self.data_dict[key]]
                    print("\n\nРезультат поиска:\n")
                            
                    self.print_record(record)
                    
                return count

        return -1


    def parse_full_search(self, key, output = True):
        count = self.full_search(key, output)
        
        if (output):
            print("Полный перебор:\nКоличество сравнений: ", count if (count != -1) else "Не найдено")

        return count
    

    def sort_dict(self, to_sort_dict):
        keys = list(to_sort_dict.keys())
        keys.sort()

        tmp_dict = dict()

        for key in keys:
            tmp_dict[key] = to_sort_dict[key]

        return tmp_dict

    
    def parse_binary_search(self, key, output = True):

        sorted_dict = self.sort_dict(self.data_dict)

        count = self.binary_search(key, sorted_dict, output)

        if (output):
            print("Бинарный поиск:\nКоличество сравнений: ", count if (count != -1) else "Не найдено")

        return count


    def binary_search(self, key, sorted_dict, output = True):
        count = 0 # count of comparsions

        keys = list(sorted_dict.keys())

        left = 0 
        right = len(keys)

        while (left <= right):
            count += 1
            middle = (left + right) // 2
            elem = keys[middle]

            if (elem == key):
                if (output):
                    record = [key, sorted_dict[key]]
                    print("\n\nРезультат поиска:\n")     
                    self.print_record(record)
                    
                return count

            if (elem < key):
                left = middle + 1
            else:
                right = middle - 1

        return -1


    def sort_value(self, diction):
        sorted_dict = dict()

        # sorted by value dict items
        items = list(diction.items())
        items.sort(key = lambda k: k[1], reverse = True)

        for elem in items:
            sorted_dict[elem[0]] = elem[1]

        return sorted_dict


    def make_segments(self):
        temp_dict = {i: 0 for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}

        for key in self.data_dict:
            temp_dict[key[FIRST_LETTER]] += 1

        temp_dict = self.sort_value(temp_dict)

        segmented_dict = {i: dict() for i in temp_dict}

        for key in self.data_dict:
            segmented_dict[key[0]].update({key: self.data_dict[key]})

        return segmented_dict

    
    def segment_search(self, key, segmented_dict, output = True):
        count = 0

        keys = list(segmented_dict.keys())

        for key_letter in keys:
            count += 1

            if (key[FIRST_LETTER] == key_letter):
                count_search = 0

                for elem in segmented_dict[key_letter]:
                    count_search += 1

                    if (elem == key):
                        if (output):
                            record = [key, segmented_dict[key_letter][key]]
                            print("\n\nРезультат поиска:\n")     
                            self.print_record(record)

                        return count_search + count

                return -1

        return -1


    def parse_segment_search(self, key, output = True):

        segmented_dict = self.make_segments()

        count = self.segment_search(key, segmented_dict, output)

        if (output):
            print("Поиск сегментами:\nКоличество сравнений: ", count if (count != -1) else "Не найдено")

        return count


    def parse_all(self, key):
        self.parse_full_search(key)
        self.parse_binary_search(key)
        self.parse_segment_search(key)