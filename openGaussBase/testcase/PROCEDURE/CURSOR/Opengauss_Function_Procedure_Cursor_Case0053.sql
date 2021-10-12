-- @testpoint: 游标先声明后定义,输入参数为bool类型

--游标用例准备的表数据
drop table if exists emp;
create table emp(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp values(1,'zhangsan','doctor1',10000),(2,'zhangsan2','doctor2',10000),(123,'zhangsan3','doctor3',10000);

--游标先声明后定义
create or replace procedure p_emp_001(str boolean)
as
declare
    a emp%rowtype;
    cursor mycursor is  select * from emp where empno=1 order by ename;
begin
    open mycursor;
    fetch  mycursor into a;
    close mycursor;
end;
/
call p_emp_001(true);
drop procedure p_emp_001;
drop table emp;




