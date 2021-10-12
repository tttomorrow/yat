-- @testpoint: 游标绑定的select含子select子句

drop table if exists emp;
create table emp(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp values(1,'zhangsan','doctor1',10000),(2,'zhangsan2','doctor2',10001),(3,'zhangsan3','doctor3',10002);
insert into emp values(1,'zhansi','doctor1',10003),(2,'lisiabc','doctor2',10004),(3,'zhangwu123','doctor3',10005);

create or replace procedure p_emp_011(str boolean)
as
declare
    a emp%rowtype;
    cursor mycursor is  select * from emp where emp.ename in(select ename from emp where emp.empno=1) order by ename;
begin
    open mycursor;
    loop
    if  mycursor%isopen then
        update emp set job='teacher' where empno=3;
        fetch mycursor into a;
    end if;
    exit
    when  mycursor%notfound;
    update emp set job='student' where empno=2;
    end loop;
end;
/
call p_emp_011(true);
select * from emp;
drop procedure p_emp_011;
drop table emp;