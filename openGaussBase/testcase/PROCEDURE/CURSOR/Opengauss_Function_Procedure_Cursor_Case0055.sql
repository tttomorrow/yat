-- @testpoint: open后不close游标

drop table if exists emp;
create table emp(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp values(1,'zhangsan','doctor1',10000),(2,'zhangsan2','doctor2',10000),(123,'zhangsan3','doctor3',10000);

create or replace procedure p_emp_003(str boolean)
AS
declare
    a emp%rowtype;
    cursor mycursor is  select * from emp where empno=1 order by ename;
begin
    open mycursor;
    fetch  mycursor into a;
    raise info'a:%',a;
end;
/
call p_emp_003(true);
drop procedure p_emp_003;
drop table emp;