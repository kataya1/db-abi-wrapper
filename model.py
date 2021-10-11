

# con = psycopg2.connect(database='iti_python', user='postgres', password='postgres',
#                        host='127.0.0.1', port='5432')

# print('database connection successful 💪')


import psycopg2
import functools

class db:
    def __init__(self, database, user, password, host, port):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def connect(self, func):
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            try:
 
                con = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.host, port=self.port)
                cursor = con.cursor()
                # print('args in wrapper ',args)
                # print('kwargs in wrapper ',kwargs)
                func(cur=cursor,*args,**kwargs)
                con.commit()
                # maybe passing cur=currsor like that isn't that best way
                # args[0].__setattr__('cur',cursor); func(*args, **kwargs) #where args is the obj(self) #wont work on a class method
                #     or
                # wrapper(obj,*args,**kwargs); obj.cur = cursor; func(obj,*args,**kwargs); self.cur = 
                # --------
            except Exception as e:
                print(f'⚠⚠⚠ error: {e}')
                con.rollback()
            finally:
                con.close()
        return wrapper

    def initialize_db(self, sql):
        con = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.host, port=self.port)
        con.set_isolation_level(2)
        cursor = con.cursor()
        cursor.execute(sql)
        # cursor.execute('alter table department add constraint fk_fk foreign key (manager_id) references employee(id);')
        con.commit()
        con.close()
            

class table:
    def __init__(self, table_name, db__obj, num_columns, **kwargs):
        self.table_name = table_name

        # table.db_obj = db__obj
        self.db_obj = db__obj
        self.num_columns = num_columns
        self.table_properties = kwargs
        '''
        for key, value in kwargs.items():
            # print(f'kwargs ---> {key}, {value}')
            self.__setattr__(key, value)
            # self.(key) = value
            # TODO when you pass a column as kwargs maybe the text will be forignkey table_name(col) filter this to be added on a separate row. maybe primary key too
        ''' # this was cool but it's not the right way
        # self.__create()

    # what the heck did i creat what is this!?? why is this!?? (double double wrapper) 
    def connect(func):
        @functools.wraps(func)
        def wrapper(self, *args,**kwargs):
            # why does it know db_obj now ? #ans it was getting the global object defined down with the same variable name so i change it down there
            self.db_obj.connect(func)(self, *args,**kwargs)
        return wrapper

    # maybe this whole function is stupid i don't remember why i created it this way
    # @classmethod #how does a class access the attributes of the instance? #ans: well it gonna be called in an instance method pass the self.vars to it #nvm 
    # @connect
    # @db_obj.connect #why does it notw kno db_obj
    def __create(self, cur=None):
        'create a new table. an instance dont create anything only the class does when instantiating'

        if len(self.table_properties['columns']) != self.num_columns:
            raise Exception('number of columns specified and len of columns in table_properties doesn\'t match')
        cur.execute(f'''
        create table if not exists {self.table_name}(
            {', '.join([f'{k} {v}' for k,v in self.table_properties['columns'].items()])},
            {', '.join(self.table_properties['table_constraints'])}
        );''')

        
    # CRUD
    @connect
    def insert(self, cur=None, **kwargs ):
        'insert a record into the table'
        # print(','.join(kwargs.keys()))
        # print(kwargs)
        # print(kwargs)
        # print(','.join(kwargs.keys()))
        # print(kwargs.values())
        # print(','.join( [ (f" '{v}' " if type(v) == str else f" {v} ") for v in kwargs.values() ] ))
        
        cur.execute(f'''insert into {self.table_name}({','.join(kwargs.keys())}) values({','.join( [ (f" '{v}' " if type(v) == str else f" {v} ") for v in kwargs.values() ] )});''')

    @connect
    def read(self,query, cur=None):
        'a select statement'
        cur.execute(query)
        for emp in cur.fetchall():
            print(emp)
        print('-------')
        
    @connect
    def update(self, cur=None, where = '',**kwargs):
        'update the volues of a column in the table(NOT IMPLEMENTED)'
        setters = ','.join([f"{key} = '{value}'" for key, value in kwargs.items()])
        cur.execute(f"update {self.table_name} set {setters} {f'where  {where}' if where else '' };")

    @connect
    def delete(self, cur=None, where = ''):
        'drop row(IN TABLE)'
        cur.execute(f"delete from {self.table_name} {f'where  {where}' if where else '' };")

        
    @connect
    def alter(self, query, cur=None):
        'change table add/drop/modify column(NOT IMPLEMENTED'
        cur.execute(query)

    @connect
    def drop(self, cur=None, options=''):
        'drop table'
        cur.execute(f'drop table if exists {self.table_name} {options};')

    
    # cur is passed from the wraper functtion
    @connect
    def truncate(self,options='',cur=None):
        'remove all entries from table'
        #we only havea one statement related to the functionality that means it's time for a wrapper/ decorator
        cur.execute(f'truncate table {self.table_name} {options};') 

    


if __name__ == "__main__":

    emp_table_properties = {
        'columns': {
                    'id': 'serial primary key',
                    'first_name':'text not null',
                    'last_name':'text',
                    'DOB': 'date',
                    'departement': 'varchar(50) null',
                    'salary': 'numeric(10,3)'
                    },
        'table_constraints': ['foreign key (department) references department(name) INITIALLY DEFERRED']
    }

    department_table_properties = {
        'columns': {
                    'name': 'text primary key',
                    'manager_id': 'int null'
        },
        'table_constraints': ['foreign key (manager_id) references employee(id) INITIALLY DEFERRED']
    }
    try:
        dbobj = db(database='oop_psycopg2', user='postgres', password='postgres',host='127.0.0.1', port='5432')
        dbobj.initialize_db( '''
                create table if not exists department(
                        name text primary key,
                        manager_id int
                    );
                create table if not exists employee(
                        id serial primary key,
                        first_name text not null,
                        last_name text,
                        DOB date,
                        department varchar(50) ,
                        salary numeric(10,3),
                        foreign key (department) references department(name));''' )
                        
        department_table = table('department',dbobj, 2, **department_table_properties)
        emp_t = table('employee',dbobj, 6, **emp_table_properties)
        emp_t.truncate()
        emp_t.insert(**{'first_name':'jimmy', 'dob':'4-5-1987', 'salary':37888})
        emp_t.insert(**{'first_name':'jane', 'dob':'4-5-1907', 'salary':37388})
        emp_t.insert(**{'first_name':'john', 'dob':'4-3-1977', 'salary':50008})
        emp_t.insert(**{'first_name':'falco', 'dob':'4-5-1957', 'salary':37888})
        emp_t.insert(**{'first_name':'reyner', 'dob':'4-5-1887', 'salary':37888.8}, last_name='fred')
        emp_t.read('select * from employee')
        emp_t.update(**({'last_name':'neutron', 'salary': 100000}) , where="first_name = 'jimmy'" )
        emp_t.delete(where= "first_name = 'john'")
        emp_t.read('select * from employee')
        # emp_t.read('select * from employee')


    except Exception as e:
        print(e)


'''
create table if not exists employee(
    id serial primary key,
    first_name text not null,
    last_name text,
    DOB date,
    department varchar(50) ,
    salary numeric(10,3),
    foreign key (department) references department(name)
);

create table department(
    name text primary key,
    manager_id int,
    foreign key (manager_id) references employee(id) 
);

'''

# create table employee( id serial primary key);