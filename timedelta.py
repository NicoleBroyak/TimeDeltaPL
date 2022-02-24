from calendar import month
from datetime import datetime

class TimeDeltaPL:
    """Class used to convert difference between dates into polish language"""

    def __init__(self):
        self.author = 'Nicole Broyak'
        self.difference_boolean_control = True

    @staticmethod
    def translation_dependency_tuple():
        """if part of date is here, the numeral will be written adequately"""
        return (2, 3, 4, 22, 23, 24, 32, 33, 34, 42, 43, 44, 52, 53, 54)

    @staticmethod
    def translation_endings():
        return {
            0: ['rok', 'lat', 'lata'], #years
            1: ['miesiąc', 'miesięcy', 'miesiące'], #months
            2: ['dzień', 'dni', 'dni'], #days
            3: ['godzinę', 'godzin', 'godziny'], #hours
            4: ['minutę', 'minut', 'minuty'], #minutes
        }

    def conversion_values(self, month):
        return {
                0: 12, #mo
                1: self.months_lengths()[month - 1], #days
                2: 24, #hours
                3: 60, #minutes
                }

    @staticmethod
    def months_lengths():
        return (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

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

        num_list, differences = self.create_date_differences_list(date_1, date_2)
        differences = self.process_date_differences_list(differences, num_list)
        print(self.translate_date_difference(differences))
        self.difference_boolean_control = False

    @staticmethod
    def convert_attr_to_date_list(date_num):
        """Converts iso-formatted date-string to splitted list"""

        return [
            int(date_num[:4]),
            int(date_num[6:7]) if date_num[5] == '0' else int(date_num[5:7]),
            int(date_num[9:10]) if date_num[8] == '0' else int(date_num[8:10]),
            int(date_num[12:13]) if date_num[11] == '0' else int(date_num[11:13]),
            int(date_num[14:16]) if date_num[14] == '0' else int(date_num[14:16])
        ]    

    def dates_numeric_lists(self, date_1: str, date_2: str) -> list:
        """Creates list of splitted lists"""

        return [self.convert_attr_to_date_list(date_1),
                self.convert_attr_to_date_list(date_2)]

    @staticmethod
    def create_difference_template(list, index):
        """Method to create raw differences used in other methods"""
        return list[0][index] - list[1][index]

    def create_date_differences_list(self, date_1: str, date_2: str) -> list:
        num_list = self.dates_numeric_lists(date_1, date_2)
        print(num_list)
        return [num_list, [self.create_difference_template(num_list, i) for i in range(5)]]

    def boolean_checker(self, diffs):
        """Temporary way to fix bugs related to differences"""

        if (any(i < 0 for i in diffs[3:]) and all(i >= 0 for i in diffs[:2])):
            self.difference_boolean_control = True
        if (any(i >= 0 for i in diffs[3:]) and all(i < 0 for i in diffs[:2])):
            self.difference_boolean_control = True


    def process_date_differences_list(
        self, differences: list, num_list: list) -> list:
        """Main method used to obtain correct differences list"""

        temp = differences[:]
        self.boolean_checker(temp)
        return [temp[4] if i == 4 else self.check_difference_template(temp, num_list, i) 
                for i in range(5)]

    def check_difference_template(
        self, diffs: list, numeric_list: list, index: int) -> int:
        """Method used to correctly calculate raw differences. To split into
        smaller methods in the process of refactoring"""

        convert_values = self.conversion_values(numeric_list[0][1])
        """if ((diffs[index] > 0 and diffs[index+1] < 0)
        or (diffs[index] > 0 and index > 0 and diffs[index - 1] < 0)
        ):
            if index > 2 and not self.difference_boolean_control:
                return diffs[index]
            diffs[index] -= 1
            diffs[index+1] += convert_values[index]
            return diffs[index]
        elif ((diffs[index] < 0 and diffs[index+1] > 0)
        or (diffs[index] < 0 and index > 0 and diffs[index - 1] > 0)
        ):
            if index > 2 and not self.difference_boolean_control:
                return diffs[index]
            diffs[index] += 1
            diffs[index+1] -= convert_values[index]
            return diffs[index]
        else:
            return diffs[index]"""
        return diffs[index]

    def past_present_or_future_checker(self, differences):
        for i in differences: return -1 if i < 0 else 1

    def assemble_translation(self, list_to_assemble, differences):
        assembled = ''
        for piece in list_to_assemble: assembled += piece
        if self.past_present_or_future_checker(differences) == -1:
            return f'Wydarzenie odbyło się {assembled[:-2]} temu.'
        elif all(i == 0 for i in differences):
            return 'Wydarzenie odbywa się teraz.'
        elif self.past_present_or_future_checker(differences) == 1:
            return f'Wydarzenie odbędzie się za: {assembled[:-2]}.'

    def translate_difference_template(self, index, difference, endings):
        """Method used to create singular or plural Polish numeral """
        abs_value = abs(difference[index])
        if abs_value == 1:
            return f'{abs_value} {endings[0]}, '
        elif abs_value in self.translation_dependency_tuple():
            return f'{abs_value} {endings[2]}, '
        elif difference[index] != 0:
            return f'{abs_value} {endings[1]}, '
        return ''

    def translate_date_difference(self, differences):
        """Main method comprised of sub-methods needed to translate date diff"""
        
        d, endings = differences, self.translation_endings()
        return self.assemble_translation(
        [self.translate_difference_template(i, d, endings[i]) for i in range(5)],
        differences
        )

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
