from model import table, db
class employee:
    employee_list = {}
    table_emp = None
    def __init__(self,first_name, last_name, DOB, department, salary):
        self.first_name =first_name
        self.last_name = last_name
        self.DOB = DOB 
        self.department = department
        self.salary = salary

        # TODO ■ Insert new record in table employee in database
        employee.table_emp.insert(**{'first_name':first_name, 'last_name':last_name, 'dob':DOB, 'department': department, 'salary':salary})
        res = employee.table_emp.read(f'select id from employee order by id desc limit 1;')
        self.id = res[0][0]
        employee.employee_list[self.id] = self

    def transfer(self,new_dept):
        self.department = new_dept
        # TODO Update the database record with the update
        employee.table_emp.update( **{'department':new_dept}, where=f'id = {self.id}')

    def fire(self):
        del employee.employee_list[self.id]
        # TODO
        # ■ Delete its record from the database
        employee.table_emp.delete(where=f'id = {self.id}')

    
    def __str__(self):
        return f'id: {self.id}, name: {self.first_name} {self.last_name}, DOB: {self.DOB}, department: {self.department}, salary: {self.salary}'

    def show(self):
        print(self)
    
    @staticmethod
    def list_employees():
        for emp in employee.employee_list.values():
            print(emp)
    
    # there should be a department table  
    # there shouldn't be a manager table because a manager is an employee and he manages a dept in a 1 to 1 may-must relationship. 
    # the department table should have the manager id.
    # age is a derived attribute it should be ignored
    # just work with this badly designed database for now man. i wanna finish and sleep

class manager(employee):
    def __init__(self,first_name, last_name, DOB, department, salary, managed_department):
        super().__init__(first_name, last_name, DOB, department, salary)
        self.managed_department = managed_department


    

    def __str__(self):
        return f'id: {self.id}, name: {self.first_name} {self.last_name}, DOB: {self.DOB}, department: {self.department}, managed department: {self.managed_department}, salary: "classified"'

def setup():
    dbobj = db(database='oop_psycopg2', user='postgres', password='postgres',host='127.0.0.1', port='5432')
    dbobj.reset_db()

    department_table_properties = {
        'columns': {
                    'name': 'text primary key',
                    'manager_id': 'int'
        },
        'table_constraints': []
    }
    emp_table_properties = {
        'columns': {
                    'id': 'serial primary key',
                    'first_name':'text not null',
                    'last_name':'text',
                    'DOB': 'date',
                    'department': 'varchar(50)',
                    'salary': 'numeric(10,3)'
                    },
        'table_constraints': []
    }
    
        # 'table_constraints': ['foreign key (department) references department(name)'] #

    table_department = table('department',dbobj, 2, department_table_properties)
    emp_t = table('employee',dbobj, 6, emp_table_properties)
    # table_department.alter('alter table department add constraint fk_fk foreign key (manager_id) references employee(id);')
    employee.table_emp = emp_t
    employee('john', 'doe', '2-5-1978', 'Accounting', 30000)
    manager('jane', 'doe', '4-9-1944', 'Management', 230000.22, 'Accounting')

def main():
    def hire():
        w = input('\nso you wanna hire!, Ok\t e for employee, m for manager, what\'s it gonna be? ')
        print('Employee:' if w == 'e' else ('Manager:' if w == 'm' else 'what\'s that!? bye!'))
        inp = {'first_name': '', 'last_name': '', 'DOB': 'format(dd-mm-yyyy)', 'department': '', 'salary': ''}
        for key, value in inp.items():
            inp[key] = input(f'please enter {key} {value}:')
        inp['salary'] = int(inp['salary'])
        if w == 'm':
            inp['managed_department'] = input('please enter managed department? ')
            manager(**inp)
        elif w == 'e':
            employee(**inp)
        
    def transfer():
        eid = input('id? ')
        employee.employee_list[int(eid)].transfer(input('new department? '))
    def listemp():
        employee.list_employees()
    def fire():
        employee.employee_list[int(input('input employee id: '))].fire()
    def quitgame():
        return 1

    menu ={
        'hire': hire,
        'transfer': transfer,
        'fire': fire,
        'list': listemp,
        'q': quitgame,
        
    }
    def game():
        print('hello there\nhere is what you can do:\n\t\t\t\t\t\tkeywords\n"hire": hire new employee enter\t"transfer": transfer employee to another department\t"fire": you know what it does\t"list": list info about all employees')
        userin = input('\nso what\'re you gonna do? ')
        if userin in menu:
            quit_flag = menu[userin]()
        if quit_flag == 1:
            print('bye')
            return
        else:
            print("-------------------------------------------\n")
            return game()
    game()

if __name__ == '__main__':
    try:
        setup()
        main()
    except Exception as e:
        print(e)