from datetime import datetime

class TimeDeltaPL:
    """Class used to convert difference between dates into polish language"""

    def __init__(self):
        self.author = 'Nicole Broyak'
        self.create_months_lengths()
        self.create_translation_dependency_tuple()
        self.difference_boolean_control = True

    def create_translation_dependency_tuple(self):
        """if part of date is here, the numeral will be written adequately"""

        self.translation_dependencies = (2, 3, 4, 22, 23, 24, 32, 33, 34,
        42, 43, 44, 52, 53, 54)

    def create_months_lengths(self):
        self.months_lengths = {
            '1': 31, '2': 28, '3': 31, '4': 30, '5': 31, '6': 30
            ,'7': 31, '8': 31, '9': 30, '10': 31, '11': 30, '12': 31
        }

    def make_asterisks(callback, *args):
        """Simple decorator to make asterisks above and below methods"""

        def retfunc(*args):
            print("*" * 50)
            callback(*args)
            print("*" * 50 + '\n')
        return retfunc

    @make_asterisks
    def convert_date_to_pl(self, date_1, date_2=str(datetime.now())):
        """Main method composed from every sub-methods"""

        self.create_dates_numeric_lists(date_1, date_2)
        print(self.date_numeric_list)
        self.create_date_differences_list(self.date_numeric_list)
        self.process_date_differences_list()
        self.translate_date_difference()
        self.clear_attributes()

    def clear_attributes(self):
        """Method used while performing test runs"""

        self.date_numeric_list = []
        self.differences = []
        self.difference_boolean_control = False


    def convert_attr_to_date_list(self, date_num):
        """Converts iso-formatted date-string to splitted list"""

        return [
            int(date_num[:4]),
            int(date_num[6:7]) if date_num[5] == '0' else int(date_num[5:7]),
            int(date_num[9:10]) if date_num[8] == '0' else int(date_num[8:10]),
            int(date_num[12:13]) if date_num[11] == '0' else int(date_num[11:13]),
            int(date_num[14:16]) if date_num[14] == '0' else int(date_num[14:16])
        ]    

    def create_dates_numeric_lists(self, date_1, date_2):
        """Creates list of splitted lists"""

        self.date_numeric_list = [
            self.convert_attr_to_date_list(date_1),
            self.convert_attr_to_date_list(date_2)
        ]
    def create_date_differences_list(self, list):
        self.differences = []
        self.differences.append(self.create_difference_template(list, 0))
        self.differences.append(self.create_difference_template(list, 1))
        self.differences.append(self.create_difference_template(list, 2))
        self.differences.append(self.create_difference_template(list, 3))
        self.differences.append(self.create_difference_template(list, 4))


    def boolean_checker(self, diffs):
        """Temporary way to fix bugs related to differences"""

        if (any(i < 0 for i in diffs[3:]) and all(i >= 0 for i in diffs[:2])):
            self.difference_boolean_control = True
        if (any(i >= 0 for i in diffs[3:]) and all(i < 0 for i in diffs[:2])):
            self.difference_boolean_control = True


    def process_date_differences_list(self):
        """Main method used to obtain correct differences list"""

        diffs = self.differences[:]
        self.boolean_checker(diffs)
        self.differences = []
        self.differences.append(self.check_difference_template(diffs, 0))
        self.differences.append(self.check_difference_template(diffs, 1))
        self.differences.append(self.check_difference_template(diffs, 2))
        self.differences.append(self.check_difference_template(diffs, 3))
        self.differences.append(diffs[4])

    def check_difference_template(self, diffs, index):
        """Method used to correctly calculate raw differences. To split into
        smaller methods in the process of refactoring"""

        convert_values = {
            '0': 12, 
            '1': self.months_lengths[str(self.date_numeric_list[0][1])],
            '2': 24,
            '3': 60}
        if ((diffs[index] > 0 and diffs[index+1] < 0)
        or (diffs[index] > 0 and index > 0 and diffs[index - 1] < 0)
        ):
            if index > 2 and not self.difference_boolean_control:
                return diffs[index]
            diffs[index] -= 1
            diffs[index+1] += convert_values[str(index)]
            return diffs[index]
        elif ((diffs[index] < 0 and diffs[index+1] > 0)
        or (diffs[index] < 0 and index > 0 and diffs[index - 1] > 0)
        ):
            if index > 2 and not self.difference_boolean_control:
                return diffs[index]
            diffs[index] += 1
            diffs[index+1] -= convert_values[str(index)]
            return diffs[index]
        else:
            return diffs[index]

    def translate_date_difference(self):
        """Main method comprised of sub-methods needed to translate date diff"""

        self.translation = ''
        self.translate_difference_template(0, 'rok', 'lat', 'lata')
        self.translate_difference_template(1, 'miesiąc', 'miesięcy', 'miesiące')
        self.translate_difference_template(2, 'dzień', 'dni')
        self.translate_difference_template(3, 'godzinę', 'godzin', 'godziny')
        self.translate_difference_template(4, 'minutę', 'minut', 'minuty')
        self.insert_time_of_occurence_sentences()
        print(self.translation)

    def insert_time_of_occurence_sentences(self):
        if self.past_present_or_future_checker() == -1:
            self.translation = 'Wydarzenie odbyło się ' + self.translation
            self.translation += 'temu'
        else:
            self.translation = 'Wydarzenie odbędzie się za ' + self.translation
            if self.translation == 'Wydarzenie odbędzie się za ':
                self.translation = 'Wydarzenie odbywa się teraz'
        
    def past_present_or_future_checker(self):
        for i in self.differences:
            if i == 0: continue
            else: return -1 if i < 0 else 1

    def translate_difference_template(self, index, ending_1, ending_2, ending_3=''):
        """Method used to create singular or plural Polish numeral """
        if abs(self.differences[index]) == 1:
            self.translation += f'{abs(self.differences[index])} {ending_1} '
        elif (ending_3
        and abs(self.differences[index]) in self.translation_dependencies):
            self.translation += f'{abs(self.differences[index])} {ending_3} '
        elif self.differences[index] == 0:
            return
        else: self.translation += f'{abs(self.differences[index])} {ending_2} '
        

    def create_difference_template(self, list, index):
        """Method to create raw differences used in other methods"""
        if list[0][index] != list[1][index]:
            return list[0][index] - list[1][index]
        else:
            return 0

#example tests
z = TimeDeltaPL()
z.convert_date_to_pl('2032-03-03 01:12', '2022-02-03 21:00')
z.convert_date_to_pl('2032-01-03 01:12', '2022-02-03 21:00')
z.convert_date_to_pl('2024-12-22 23:15', '2022-02-03 21:00')
z.convert_date_to_pl('2022-07-11 15:22', '2022-02-03 21:00')
z.convert_date_to_pl('2022-02-03 23:35', '2022-02-03 21:00')
z.convert_date_to_pl('2022-02-03 18:25', '2022-02-03 21:00')
z.convert_date_to_pl('2021-11-05 14:59', '2022-02-03 21:00')
z.convert_date_to_pl('2020-08-17 08:05', '2022-02-03 21:00')
z.convert_date_to_pl('2024-01-01 23:31', '2024-01-01 23:31')
z.convert_date_to_pl('2024-01-01 23:29', '2024-01-01 23:31')
z.convert_date_to_pl('2024-01-01 23:33', '2024-01-01 23:31')
z.convert_date_to_pl('2024-02-28 23:33', '2025-02-28 23:32')
z.convert_date_to_pl('2024-02-28 23:33', '2025-02-28 23:34')
z.convert_date_to_pl('2026-02-28 23:33', '2025-02-28 23:32')
z.convert_date_to_pl('2026-02-28 23:33', '2025-02-28 23:34')
