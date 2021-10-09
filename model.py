
class employee:
    employee_list = []
    def __init__(self,first_name, last_name, age, department, salary):
        self.first_name =first_name
        self.last_name = last_name
        self.age = age
        self.department = department
        self.salary = salary
        employee.employee_list.append(self)
        # TODO ■ Insert new record in table employee in database

    def transfer(self,new_dept):
        self.department = new_dept
        # TODO Update the database record with the update

    def fire(self):
        employee.employee_list.remove(self)
        # TODO
        # ■ Delete its record from the database
    
    def __str__(self):
        return f'name: {self.first_name} {self.last_name}, age: {self.age}, department: {self.department}, salary: {self.salary}'

    def show(self):
        print(self)
    
    @staticmethod
    def list_employees():
        for emp in employee.employee_list:
            print(emp)
        
    # there should be a department table  
    # there shouldn't be a manager table because a manager is an employee and he manages a dept in a 1 to 1 may-must relationship. 
    # the department table should have the manager id.
    # age is a derived attribute it should be ignored
    # just work with this badly designed database for now man. i wanna finish and sleep

class manager(employee):

    def __init__(self,first_name, last_name, age, department, salary, managed_department):
        super().__init__(first_name, last_name, age, department, salary)
        self.managed_department = managed_department

    def __str__(self):
        return f'name: {self.first_name} {self.last_name}, age: {self.age}, department: {self.department}, salary: "classified"'
        



if __name__ == '__main__':
    emp1 = employee('john','doe',32,'Accounting', 30000)
    mang1 = manager('jane', 'doe', 56, 'Management', 150000, 'Accounting')

    # emp1.show()
    # mang1.show()
 

    mang1.list_employees()
    # manager.list_employees()
