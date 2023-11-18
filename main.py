from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if value:
            self.__value = value
        else:
            raise ValueError

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):

    def value(self, value):
        if len(value) == 10 and int(value):
            self.__value = value
        else:
            raise ValueError


class Birthday(Field):

    def value(self, value):
        if datetime.strptime(value, '%d.%m.%Y'):
            self.__value = value
        else:
            raise ValueError

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)
    
    def add_phone(self, number):
        self.phones.append(Phone(number))

    def remove_phone(self, number):
        for num in self.phones:
            if num.value == number:
                self.phones.remove(num)

    def edit_phone(self, number, new_number):
        check_flag = False
        for ind, phone in enumerate(self.phones):
            if phone.value == number:
                self.phones[ind] = Phone(new_number)
                check_flag = True
            if not check_flag:
                raise ValueError

    def find_phone(self, number):
        for num in self.phones:
            if num.value == number:
                return num
            
    def days_to_birthday(self):
        today_date = datetime.now()
        birthday_to_date = datetime.strptime(self.birthday.value, '%d.%m.%Y')
        this_year = birthday_to_date.replace(year=today_date.year)
        next_year = birthday_to_date.replace(year=today_date.year+1)
        if this_year.timestamp()-today_date.timestamp() < 0:
            return (next_year - today_date).days
        else:
            return (this_year - today_date).days


    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday.value}"
    
# class Iterable:
#     def __init__(self, address_book, N):
#         self.current_value = 0
#         self.address_book = address_book
#         self.max = N

#     def __next__(self):
#         result = []
#         for record in self.address_book.values():
#             if self.current_value <= self.max:
#                 result.append(Record.__str__(record))
#                 # result.append(record)
#                 self.current_value += 1
#             else:
#                 raise StopIteration
#         return result


class AddressBookIterator:
    def __init__(self, address_book, N):
        self.current_value = 0
        self.address_book = address_book
        self.max = N
        self.records = list(address_book.values())

    def __iter__(self):
        return self
    
    def __next__(self):
        result = []
        for record in self.address_book.values():
            if self.current_value <= self.max:
                result.append(record)
                self.current_value += 1
            else:
                raise StopIteration
        return result
        # if self.current_value >= len(self.records):
        #     raise StopIteration
        # result = []
        # for index in range(self.current_value, self.current_value+self.max):
        #     result.append(self.records[index])
        # self.current_value += self.max
        # return result
        

class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record
        
    def find(self, name):
        for key in self.data:
            if key == name:
                return self.data[name]

    def delete(self, name):
        for key in list(self.data.keys()):
            if str(key) == name:
                del self.data[key]
    
    def iterator(self, N=1):
        return AddressBookIterator(self.data, N)
        # result = []
        # counter = 1
        # for record in self.data.values():
        #     if counter <= N:
        #         result.append(Record.__str__(record))
        #         # result.append(record)
        #         counter += 1
        # return result

        


if __name__ == '__main__':
    book = AddressBook()
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    book.add_record(john_record)
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)
    for name, record in book.data.items():
        print(name, record)
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")
    book.delete("Jane")
    vicky_record = Record("Vicky", "23.03.1996")
    vicky_record.add_phone("7777777777")
    book.add_record(vicky_record)
    vicky = book.find("Vicky")
    print(vicky.days_to_birthday())
    print(book.iterator(3))
    