-- @testpoint: 隐式游标%notfound，提取不到数据

drop table if exists emp;
create table emp(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp values(1,'zhangsan','doctor1',10000),(2,'zhangsan2','doctor2',10000),(123,'zhangsan3','doctor3',10000);

create or replace procedure p_emp_005(str boolean)
as
declare
    a emp%rowtype;
    cursor mycursor is  select * from emp where empno=1 order by ename;
begin
    open mycursor;
    fetch  mycursor into a;
    if mycursor%notfound then
        insert into emp values(4,'zhangsan','doctor1',10002);
    end if;
    close mycursor;
end;
/
call p_emp_005(true);
select * from emp;
drop procedure p_emp_005;
drop table emp;