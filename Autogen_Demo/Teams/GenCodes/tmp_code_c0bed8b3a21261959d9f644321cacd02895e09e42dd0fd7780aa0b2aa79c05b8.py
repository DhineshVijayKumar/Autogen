class Employee:
    def __init__(self, name, position):
        self.name = name
        self.position = position

    def display_info(self):
        print(f"Employee Name: {self.name}")
        print(f"Position: {self.position}")

# Example usage
employee1 = Employee("John Doe", "Software Engineer")
employee1.display_info()
