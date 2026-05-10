# Project 3 - Contact Manager

## Importing libraries
import json # Handle JSON files
import os # Handle operational system directories

## Classes

### Contact Class
class Contact:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email
    
    def __str__(self):
        return f"Name: {self.name}, Phone: {self.phone}, Email: {self.email}"

    def to_dict(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email
        }

### ContactManager Class
class ContactManager:
    def __init__(self, filename = "contacts.json"):
        self.filename = filename
        self.contacts = []
        self.load_contacts()

    def load_contacts(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding='utf-8') as file:
                    data = json.load(file)
                    for item in data:
                        contact = Contact(
                            item.get("name", ""),
                            item.get("phone", ""),
                            item.get("email", "")
                        )
                        self.contacts.append(contact)
            except Exception as e:
                print(f"Error loading contacts: {e}")
        else:
            print(f"There is no file named {self.filename}.")

    def save_contacts(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump([contact.to_dict() for contact in self.contacts], file, indent=4)
        except Exception as e:
            print(f"Error saving contacts: {e}")

    def add_contact(self, contact):
        self.contacts.append(contact)
        self.save_contacts()

    def edit_contact(self, name, new_contact):
        for index, contact in enumerate(self.contacts):
            if contact.name == name:
                self.contacts[index] = new_contact
                self.save_contacts()
                return True
        return False

    def remove_contact(self, name):
        for index, contact in enumerate(self.contacts):
            if contact.name == name:
                del self.contacts[index]
                self.save_contacts()
                return True
        return False

    def list_contacts(self):
        return self.contacts
    
### Menu function
def menu():
    print("\n=== Contact Manager ===")
    print("1. List Contacts")
    print("2. Add Contact")
    print("3. Edit Contact")
    print("4. Remove contact")
    print("5. Exit")

def main():
    manager = ContactManager()

    while True:
        menu()
        option = input("Choose an option: ")
        if option == "1":
            contacts = manager.list_contacts()
            if contacts:
                for contact in contacts:
                    print(contact)
        elif option == "2":
            name = input("Name: ")
            phone = input("Phone: ")
            email = input("Email: ")
            contact = Contact(name, phone, email)
            manager.add_contact(contact)
            print(f"{name} added to the contact list!")
        elif option == "3":
            name = input("Enter the name of the contact to edit: ")
            print("Enter the new details: ")
            new_name = input("New name: ")
            new_phone = input("New phone: ")
            new_email = input("New email: ")
            new_contact = Contact(new_name, new_phone, new_email)
            if manager.edit_contact(name, new_contact):
                print("Contact updated!")
            else:
                print("Contact not found.")
        elif option == "4":
            name = input("Enter the name of the contact to remove: ")
            if manager.remove_contact(name):
                print("Contact removed!")
            else:
                print("Contact not found!")
        elif option == "5":
            print("Exiting the program.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()