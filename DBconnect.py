import psycopg2

# con = psycopg2.connect(database='iti_python', user='postgres', password='postgres',
#                        host='127.0.0.1', port='5432')

# print('database connection successful 💪')

class table:
    def __init__(self, table_name, *args, **kwargs):
        self.table_name = table_name
        for x in args:
            print("args ", x)
        for key, value in kwargs.items():
            print('kwargs ', key, value)
            self.__setattr__(key,value)
            # self.(key) = value
            # TODO when you pass a column as kwargs maybe the text will be forignkey table_name(col) filter this to be added on a separate row. maybe primary key too
        
    def create(self):
        pass

    @staticmethod
    def read(*args):
        pass

    def update(self):
        pass

    def truncate(self):
        pass

    def delete(self):
        pass

class entry(table):
    def __init__(self):
        pass
    
    def insert(self):
        pass

    def alter(self):
        pass
    
if __name__ == "__main__":
    t = table('employee', **{"first_name":['text', 'not null'], "last_name":['text']})
    try:
        print('💪',t)
        print('😂',t.first_name)
    except Exception as e:
        print(e)