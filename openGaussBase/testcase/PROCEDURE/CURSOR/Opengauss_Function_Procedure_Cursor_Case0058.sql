-- @testpoint: %isopen 判断游标是否打开

drop table if exists emp;
create table emp(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp values(1,'zhangsan','doctor1',10000),(2,'zhangsan2','doctor2',10000),(123,'zhangsan3','doctor3',10000);


create or replace procedure p_emp_006(str boolean)
AS
declare
    a emp%rowtype;
    cursor mycursor is  select * from emp where empno=1 order by ename;
begin
    if  not mycursor%isopen then
        open mycursor;
        fetch mycursor into a;
    end if;
    if  mycursor%isopen then
        update emp set job='student' where empno=1;
        close mycursor;
    end if;
end;
/
call p_emp_006(true);
select * from emp;

drop procedure p_emp_006;

drop table emp;