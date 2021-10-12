-- @testpoint: 游标绑定的select where后带in子句

drop table if exists emp;
create table emp(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp values(1,'zhangsan','doctor1',10000),(2,'zhangsan2','doctor2',10000),(123,'zhangsan3','doctor3',10000);

create or replace procedure p_emp_008(str boolean)
as
declare
    a emp%rowtype;
    cursor mycursor is  select * from emp where emp.ename in('zhangsan','zhangsan2');
begin
    open mycursor;
    loop
    if  mycursor%isopen then
        update emp set job='teacher' where empno=2;
        fetch mycursor into a;
    end if;
    exit
    when  mycursor%notfound;
    update emp set job='students' where empno=2;
    end loop;
end;
/
call p_emp_008(true);
select * from emp;
drop procedure p_emp_008;
drop table emp;
