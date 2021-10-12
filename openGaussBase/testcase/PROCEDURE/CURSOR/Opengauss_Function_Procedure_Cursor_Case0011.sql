-- @testpoint: 存储过程中游标使用 游标绑定的select含子句select

drop table if exists emp;
create table emp(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp values(1,'zhangsan','doctor1',10000),(2,'zhangsan2','doctor2',10000),(123,'zhangsan3','doctor3',10000);
insert into emp values(1,'zhansi','doctor1',10000),(2,'lisiabc','doctor2',10000),(123,'zhangwu123','doctor3',10000);
insert into emp values(10,'abc','worker',9000);
insert into emp values(716,'ZHANGSAN','leader',20000);
insert into emp values(1,'zhansi','doctor1',100),(2,'lisiabc','doctor2',100),(123,'zhangwu123','doctor3',100);

create or replace procedure syscur_011()
is
declare
    a emp%rowtype;
    cursor mycursor is  select * from emp where emp.ename in(select ename from emp where emp.empno=1) order by ename;
begin
    open mycursor;
    loop
    if  mycursor%isopen  then  raise info 'open';
        fetch mycursor into a;
    end if;
    exit
    when  mycursor%notfound;
        raise info 'a is emp:%',a.empno;
        raise info 'name:%',a.ename;
        raise info 'job:%',a.job;
        raise info 'sal:%',a.sal;
        raise info ':%',mycursor%rowcount;
    end loop;
end;
/
call syscur_011();
drop table emp;
drop procedure syscur_011;