class Employee:
    """
    A class representing an employee.

    Attributes:
        name (str): The employee's name.
        age (int): The employee's age.
        salary (float): The employee's salary.
    """

    def __init__(self, name, age, salary):
        """
        Initializes an Employee object.

        Args:
            name (str): The employee's name.
            age (int): The employee's age.
            salary (float): The employee's salary.
        """
        self.name = name
        self.age = age
        self.salary = salary

    def display_details(self):
        """
        Displays the employee's details.
        """
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Salary: ${self.salary:.2f}")

# Example usage:
if __name__ == "__main__":
    emp = Employee("John Doe", 30, 50000.0)
    emp.display_details()
