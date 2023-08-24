from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('postgresql://neutron:123456@localhost:5432/neutron')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    address = Column(String)
    salary = Column(Integer)


Base.metadata.create_all(engine)
print("成功创建表")

employee1 = Employee(name='John Doe', age=30, address='123 Main St', salary=50000)
employee2 = Employee(name='Jane Smith', age=28, address='456 Elm St', salary=60000)
session.add(employee1)
session.add(employee2)
session.commit()
print("成功插入数据")


employees = session.query(Employee).all()
print("查询结果:")
for employee in employees:
    print("ID = {}, NAME = {}, AGE = {}, ADDRESS = {}, SALARY = {}"
          .format(employee.id, employee.name, employee.age, employee.address, employee.salary))


# employee = session.query(Employee).filter_by(name='John Doe').first()
# employee.salary = 70000
# session.commit()
# print("成功更新数据")


# employee = session.query(Employee).filter_by(name='Jane Smith').first()
# session.delete(employee)
# session.commit()
# print("成功删除数据")


session.close()
engine.dispose()
print("数据库连接已关闭")