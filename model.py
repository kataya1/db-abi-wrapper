

# con = psycopg2.connect(database='iti_python', user='postgres', password='postgres',
#                        host='127.0.0.1', port='5432')

# print('database connection successful 💪')
import psycopg2
import functools

# TODO f string escaping
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
                ret = func(cur=cursor,*args,**kwargs)
                con.commit()
                return ret
                # maybe passing cur=currsor like that isn't that best way
                # args[0].__setattr__('cur',cursor); func(*args, **kwargs) #where args is the obj(self) #wont work on a class method
                #     or
                # wrapper(obj,*args,**kwargs); obj.cur = cursor; func(obj,*args,**kwargs); self.cur = 
                # --------
            except Exception as e:
                print(f'⚠⚠⚠ function: {func.__name__} | error: {e}')
                con.rollback()
            finally:
                con.close()
        return wrapper

    def initialize_db(self, sql):
        con = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.host, port=self.port)
        # read all before commiting i think instead of auto commiting
        con.set_isolation_level(2)
        cursor = con.cursor()
        cursor.execute(sql)
        # cursor.execute('alter table department add constraint fk_fk foreign key (manager_id) references employee(id);')
        con.commit()
        con.close()

    # @connect nvm this will need yet another wrapper ()
    def reset_db(self, cur=None):
        con = psycopg2.connect(database='postgres', user=self.user, password=self.password, host=self.host, port=self.port)
        con.set_isolation_level(0)
        cur = con.cursor()
        cur.execute(f'drop database if exists {self.database};')
        cur.execute(f'create database {self.database};')
        
        con.close()
            

class table:
    def __init__(self, table_name='', db__obj=None, num_columns=0, table_properties={}, create=True):
        self.table_name = table_name
        # day3: why does a table need a db object if it only uses it once #too late to think about it anyway  
        self.db_obj = db__obj
        self.num_columns = num_columns
        self.table_properties = table_properties
        '''
        for key, value in kwargs.items():
            # print(f'kwargs ---> {key}, {value}')
            self.__setattr__(key, value)
            # self.(key) = value
            # TODO when you pass a column as kwargs maybe the text will be forignkey table_name(col) filter this to be added on a separate row. maybe primary key too
        ''' # this was cool but it's not the right way
        if create:
            self.__create()

    # what the heck did i create🙃 what is this😭!?? why is this🥶!?? 
    def tb_connect(func):
        @functools.wraps(func)
        def wrapper(self, *args,**kwargs):
            # why does it know db_obj now ? #ans it was getting the global object defined down with the same variable name so i change it down there
            # self here is the table instance, it gets passe into args over there at db
            return self.db_obj.connect(func)(self, *args,**kwargs)
        return wrapper

    # maybe this whole function is stupid i don't remember why i created it this way
    # @classmethod #how does a class access the attributes of the instance? #ans: well it's gonna be called in an instance method pass the self.vars to it #nvm 
    # @db_obj.connect #why does it not know db_obj
    @tb_connect
    def __create(self, cur=None):
        'create a new table. an instance dont create anything only the class does when instantiating'

        if len(self.table_properties['columns']) != self.num_columns:
            raise Exception('number of columns specified and len of columns in table_properties doesn\'t match')
        # cur.execute(f'''
        # create table if not exists {self.table_name}(
        #     {', '.join([f'{k} {v}' for k,v in self.table_properties['columns'].items()])},
        #     {', '.join(self.table_properties['table_constraints'])}
        # );''')
        cur.execute(self.formulate_table(self.table_name, self.table_properties))
        
    # CRUD
    @tb_connect
    def insert(self, cur=None, **kwargs ):
        'insert a record into the table'
        cur.execute(f'''insert into {self.table_name}({','.join(kwargs.keys())}) values({','.join( [ (f" '{v}' " if type(v) == str else f" {v} ") for v in kwargs.values() ] )});''')

    @tb_connect
    def read(self,query, cur=None):
        'a select statement'
        cur.execute(query)
        res = cur.fetchall()
        # for emp in res:
        #     print(emp)
        # print('-------')
        return res
        
    @tb_connect
    def update(self, cur=None, where = '',**kwargs):
        'update the volues of a column in the table(NOT IMPLEMENTED)'
        setters = ','.join([f"{key} = '{value}'" for key, value in kwargs.items()])
        cur.execute(f"update {self.table_name} set {setters} {f'where  {where}' if where else '' };")

    @tb_connect
    def delete(self, cur=None, where = ''):
        'drop row(IN TABLE)'
        cur.execute(f"delete from {self.table_name} {f'where  {where}' if where else '' };")

    @tb_connect
    def alter(self, query, cur=None):
        'change table add/drop/modify column(NOT IMPLEMENTED'
        cur.execute(query) #lazy implementation

    @tb_connect
    def drop(self, cur=None, options=''):
        'drop table'
        cur.execute(f'drop table if exists {self.table_name} {options};')
    
    @classmethod
    @tb_connect
    def drop(cls, table_name, cur=None, options=''):
        'drop table'
        cur.execute(f'drop table if exists {table_name} {options};')
    
    # cur is passed from the wraper functtion
    @tb_connect
    def truncate(self,options='',cur=None):
        'remove all entries from table'
        cur.execute(f'truncate table {self.table_name} {options};') 

    @staticmethod
    def formulate_table(table_name, table_properties):
        'returns a create table sql statement from the'
        return f'''
        create table if not exists {table_name}(
            {', '.join([f'{k} {v}' for k,v in table_properties['columns'].items()])}
            {',' if table_properties['table_constraints'] else ''}
            {', '.join(table_properties['table_constraints'])}
        );'''
    
if __name__ == "__main__":

    emp_table_properties = {
        'columns': {
                    'id': 'serial primary key',
                    'first_name':'text not null',
                    'last_name':'text',
                    'DOB': 'date',
                    'department': 'varchar(50)',
                    'salary': 'numeric(10,3)'
                    },
        'table_constraints': ['foreign key (department) references department(name)']
    }

    department_table_properties = {
        'columns': {
                    'name': 'text primary key',
                    'manager_id': 'int'
        },
        'table_constraints': []
    }
        # 'table_constraints': ['foreign key (manager_id) references employee(id)']

    
    dbobj = db(database='oop_psycopg2', user='postgres', password='postgres',host='127.0.0.1', port='5432')
    dbobj.reset_db()
    
    # dbobj.initialize_db( '''
    #         create table if not exists department(
    #                 name text primary key,
    #                 manager_id int
    #             );
    #         create table if not exists employee(
    #                 id serial primary key,
    #                 first_name text not null,
    #                 last_name text,
    #                 DOB date,
    #                 department varchar(50) ,
    #                 salary numeric(10,3),
    #                 foreign key (department) references department(name));
    #         alter table department add constraint fk_fk foreign key (manager_id) references employee(id);
    #         ''' )
    # print(f'''
    #     {table.formulate_table('department', department_table_properties)}
    #     {table.formulate_table('employee', emp_table_properties)}
    #     alter table department add constraint fk_fk foreign key (manager_id) references employee(id);
    # ''')
    # dbobj.initialize_db(f'''
    #     {table.formulate_table('department', department_table_properties)}
    #     {table.formulate_table('employee', emp_table_properties)}
    # ''')
        # alter table department add constraint fk_fk foreign key (manager_id) references employee(id);
    
    # day3: we have literaly come full circle
    # d = table(db__obj=dbobj, create=False)
    # d.drop('employee', options='cascade')
    # d.drop('department', options='cascade')

    department_table = table('department',dbobj, 2, department_table_properties)
    emp_t = table('employee',dbobj, 6, emp_table_properties)
    department_table.alter('alter table department add constraint fk_fk foreign key (manager_id) references employee(id);')
    # emp_t.truncate(options='cascade')
    emp_t.insert(**{'first_name':'jimmy', 'dob':'4-5-1987', 'salary':37888})
    emp_t.insert(**{'first_name':'jane', 'dob':'4-5-1907', 'salary':37388})
    emp_t.insert(**{'first_name':'john', 'dob':'4-3-1977', 'salary':50008})
    emp_t.insert(**{'first_name':'falco', 'dob':'4-5-1957', 'salary':37888})
    emp_t.insert(**{'first_name':'reyner', 'dob':'4-5-1887', 'salary':37888.8}, last_name='fred')
    emp_t.read('select * from employee')
    emp_t.update(**({'last_name':'neutron', 'salary': 100000}) , where="first_name = 'jimmy'" )
    emp_t.delete(where= "first_name = 'john'")
    emp_t.read('select * from employee')

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