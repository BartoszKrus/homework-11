from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value)
    

class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone):
        normalized_phone = ''.join(filter(str.isdigit, str(phone)))
        if len(normalized_phone) == 9:
            phone = normalized_phone
        else:
            raise ValueError("Phone number must contain exactly 9 digits.")
        super().__init__(phone)


class Birthday(Field):
    def __init__(self, birthday=None):
        if birthday is not None:
            try:
                birthday = datetime.strptime(birthday, "%d-%m-%Y")
            except ValueError:
                raise ValueError("Birthday must be in 'dd-mm-yyyy' format.")
        super().__init__(birthday)


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.birthday = Birthday(birthday)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(phone)

    def remove_phone(self, phone):
        phone_to_remove = str(phone)
        if phone_to_remove in [str(p) for p in self.phones]:
            self.phones = [p for p in self.phones if str(p) != phone_to_remove]

    def edit_phone(self, old_phone, new_phone):
        old_phone_obj = Phone(old_phone)
        for i, phone in enumerate(self.phones):
            if str(phone) == str(old_phone_obj):
                self.phones[i] = Phone(new_phone)
                return
        print("Old phone number not found.")

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def remove_birthday(self):
        self.birthday = Birthday()

    def days_to_birthday(self):
        if self.birthday.value is None:
            return None
        now = datetime.now()
        next_birthday = datetime(now.year, self.birthday.value.month, self.birthday.value.day)
        if now > next_birthday:
            next_birthday = datetime(now.year + 1, self.birthday.value.month, self.birthday.value.day)
        return (next_birthday - now).days

    def __str__(self):
        return f"Name: {self.name}, Phones: {', '.join(map(str, self.phones))}, Birthday: {self.birthday}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
      
    def find_records(self, keyword):
        results = []
        keyword_lower = keyword.lower()
        for record in self.data.values():
            if keyword_lower == record.name.value.lower():
                results.append(record)
            else:
                for phone in record.phones:
                    if keyword_lower == str(phone).lower():
                        results.append(record)
                        break  
        return results
    
    def phone_exists(self, name, phone):
        existing_records = self.find_records(name)
        if existing_records:
            record = existing_records[0]
            return str(phone) in [str(phone_obj) for phone_obj in record.phones]
        return False
    
    def __iter__(self):
        self._current = 0
        self._records = list(self.data.values())
        return self

    def __next__(self):
        if self._current >= len(self._records):
            raise StopIteration
        result = self._records[self._current]
        self._current += 1
        return result
    
    
def main():
    """
    The main() function is responsible for managing user interaction with the phone book.
    Users can perform various operations on entries in the phone book, such as adding,
    editing, removing, searching, and displaying entries, and calculating the number of 
    days to birthdays.

    Commands:
    - '.' - End the program.
    - 'good bye', 'close', 'exit' - Terminate the program with the message "Good bye!".
    - 'hello' - Display a greeting.
    - 'add' - Add a new entry to the address book.
    - 'add phone' - Add a new phone number to an existing entry.
    - 'edit phone' - Edit an existing phone number.
    - 'remove phone' - Remove a phone number from an existing entry.
    - 'add birthday' - Add a birthday to an existing entry.
    - 'remove birthday' - Remove the birthday from an existing entry.
    - 'find' - Search for entries in the address book.
    - 'days to birthday' - Calculate the number of days until the next birthday.
    - 'show all' - Display all entries in the address book.
    """
    address_book = AddressBook()

    while True:
        command = input("Enter command: ").lower()


        if '.' in command:
            break


        elif command in ['good bye', 'close', 'exit']:
            print("Good bye!")
            break


        elif command == "hello":
            print("How can I help you?")


        elif command == "add":
            name = input("Enter name: ")
            if not name.strip():
                print("Error: Name cannot be empty.\n")
                continue
                        
            existing_records = address_book.find_records(name)
            if existing_records:
                print(f"Error: This name: {name} already exists in the address book. Please choose a different name.\n")
                continue

            else:
                record = Record(name)                
                phone = input("Enter phone number: ")
                phone_str = ''
                if phone.strip():
                    try:
                        phone = Phone(phone)
                        record.add_phone(phone)
                        phone_str = phone
                    except ValueError as e:
                        print(f"Incorrect phone number: {e}")

            birthday = input("Enter birthday (dd-mm-yyyy): ")
            birthday_str = ''
            if birthday.strip():
                try:
                    record.add_birthday(birthday)
                    birthday_str = birthday
                except ValueError as e:
                    print(f"Incorrect birthday format: {e}")
            address_book.add_record(record)
            print(f"Success: Record: {name}: {phone_str}, Birthday: {birthday_str} added successfully.\n")
                

        elif command == "add phone":
            name = input("Enter name phone: ")
            if not name.strip():
                print("Error: Name cannot be empty. Please enter a valid name.\n")
                continue
            
            existing_records = address_book.find_records(name)
            if not existing_records:
                print(f"Error: This name: {name} does not exist in the address book. Please add a new record first.\n")
            else:
                phone = input("Enter phone number: ")
                if phone.strip():
                    try:
                        phone = Phone(phone)
                        record = existing_records[0]
                        record.add_phone(phone)
                        print(f"Success: Phone number: {phone} added successfully to {name}.\n")
                    except ValueError as e:
                        print(f"Incorrect phone number: {e}")
                else:
                    print("Error: No phone number was provided. No new number added.\n")


        elif command == "edit phone":
            name = input("Enter name to edit phone number: ")
            if not name.strip():
                print("Error: Name cannot be empty. Please enter a valid name.\n")
                continue

            results = address_book.find_records(name)
            if results:
                record = results[0]
                phone = input("Enter new phone number: ")
                if phone.strip():
                    try:
                        phone = Phone(phone)
                        old_phone = input("Enter old phone number to replace: ")
                        old_phone = Phone(old_phone)
                        if str(old_phone) in [str(phone_obj) for phone_obj in record.phones]:
                            record.edit_phone(old_phone, phone)
                            print(f"Success: Phone number: {phone} updated successfully.\n")
                        else:
                            print(f"Error: Old phone number: {old_phone} not found for {name}.\n")
                    except ValueError as e:
                        print(f"Incorrect phone number: {e}")
                else:
                    print(f"Error: New phone number not provided.\n")                    
            else:
                print(f"Error: Name: {name} not found in the address book.\n")


        elif command == "remove phone":
            name = input("Enter name to remove phone number: ")
            if not name.strip():
                print("Error: Name cannot be empty. Please enter a valid name.\n")
                continue

            existing_records = address_book.find_records(name)
            if existing_records:
                record = existing_records[0]
                phone = input("Enter phone number to remove: ")
                if str(phone) in [str(phone_obj) for phone_obj in record.phones]:
                    record.remove_phone(Phone(phone))
                    print(f"Success: Phone number: {phone} removed successfully.\n")
                else:
                    print(f"Error: Phone number: {phone} not found for {name}.\n")
            else:
                print(f"Error: Name: {name} not found in the address book.\n")


        elif command == "add birthday":
            name = input("Enter name: ")
            if not name.strip():
                print("Error: Name cannot be empty. Please enter a valid name.\n")
                continue

            existing_records = address_book.find_records(name)
            if existing_records:
                record = existing_records[0]
                if record.birthday.value is None:
                    birthday = input("Enter birthday (dd-mm-yyyy): ")
                    if birthday.strip():
                        try:
                            record.add_birthday(birthday)
                            print(f"Success: Birthday: {birthday} added successfully to {name}.\n")
                        except ValueError as e:
                            print(f"Incorrect birthday format: {e}")
                    else:
                        print("Error: No birthday was provided. No new birthday added.\n")
                else:
                    print(f"Error: A birthday is already assigned to {name}. Cannot add more than one birthday.\n")
            else:
                print(f"Error: Name: {name} not found in the address book.\n")



        elif command == "remove birthday":
            name = input("Enter name to remove birthday: ")
            if not name.strip():
                print("Error: Name cannot be empty. Please enter a valid name.\n")
                continue

            existing_records = address_book.find_records(name)
            if existing_records:
                record = existing_records[0]
                if record.birthday.value is not None:
                    record.remove_birthday()
                    print(f"Success: Birthday removed successfully for {name}.\n")
                else:
                    print(f"Error: No birthday found for {name}.\n")
            else:
                print(f"Error: Name: {name} not found in the address book.\n")


        elif command == "find":
            name = input("Enter name to search: ").strip()
            phone = input("Enter phone number to search: ").strip()
            if not name.strip() and not phone.strip():
                print("Error: Name and phone number cannot be empty.\n")
                continue

            results = []
            if name and phone:
                for record in address_book.values():
                    if name.lower() == record.name.value.lower() and phone in [str(p) for p in record.phones]:
                        results.append(record)
            elif name:
                for record in address_book.values():
                    if name.lower() == record.name.value.lower():
                        results.append(record)
            elif phone:
                for record in address_book.values():
                    if phone in [str(p) for p in record.phones]:
                        results.append(record)
            if results:
                print("Success: Matching records:")
                for record in results:
                    print(record)
            else:
                print("Error: No matching records found.")


        elif command == "days to birthday":
            name = input("Enter name: ")
            if not name.strip():
                print("Error: Name cannot be empty. Please enter a valid name.\n")
                continue

            existing_records = address_book.find_records(name)
            if existing_records:
                record = existing_records[0]
                days = record.days_to_birthday()
                if days is not None:
                    print(f"Success: There are {days} days until {name}'s next birthday.\n")
                else:
                    print(f"Error: No birthday found for {name}.\n")
            else:
                print(f"Error: Name: {name} not found in the address book.\n")

        
        elif command == "show all":
            if address_book:
                print("Success: All Contacts:")
                N = 5
                records = list(address_book.data.values())
                for i in range(0, len(records), N):
                    for record in records[i:i+N]:
                        print(record)
                    if i + N < len(records):
                        input("Press enter to see the next page...\n")
                print()
            else:
                print("Error: Address book is empty.\n")


        else:
            print("Error: Invalid command. Enter the correct command.\n")


if __name__ == "__main__":
    main()