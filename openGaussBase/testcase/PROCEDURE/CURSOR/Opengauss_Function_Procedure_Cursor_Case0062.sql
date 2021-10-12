-- @testpoint: 游标绑定的selectwhere后带like_子句

drop table if exists emp;
create table emp(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp values(1,'zhangsan','doctor1',10000),(2,'zhangsan2','doctor2',10001),(3,'zhangsan3','doctor3',10002);
insert into emp values(1,'zhansi','doctor1',10003),(2,'lisiabc','doctor2',10004),(3,'zhangwu123','doctor3',10005);

create or replace procedure p_emp_010(str boolean)
as
declare
    a emp%rowtype;
    cursor mycursor is  select * from emp where emp.ename like  'zhang_' order by empno,ename,job,sal;
begin
open mycursor;
    loop
    if mycursor%isopen then
        update emp set job='teacher' where empno=2;
        fetch mycursor into a;
    end if;
    exit
    when  mycursor%notfound;
    update emp set job='students' where empno=2;
    end loop;
end;
/
call p_emp_010(true);
select * from emp;
drop procedure p_emp_010;
drop table emp;