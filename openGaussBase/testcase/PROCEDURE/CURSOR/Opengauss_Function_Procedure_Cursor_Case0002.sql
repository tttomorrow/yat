-- @testpoint: 存储过程中游标使用 %isopen

drop table if exists emp;
create table emp(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp values(1,'zhangsan','doctor1',10000),(2,'zhangsan2','doctor2',10000),(123,'zhangsan3','doctor3',10000);
insert into emp values(1,'zhansi','doctor1',10000),(2,'lisiabc','doctor2',10000),(123,'zhangwu123','doctor3',10000);
insert into emp values(10,'abc','worker',9000);
insert into emp values(716,'ZHANGSAN','leader',20000);

create or replace procedure syscur_002()
is
declare
    a emp%rowtype;
cursor mycursor is  select * from emp where empno=1 order by ename;
begin
    if  not mycursor%isopen  then
        open mycursor;
        fetch mycursor into a;
        raise info 'a is emp:%',a.empno;
        raise info 'name:%',a.ename;
        raise info 'job:%',a.job;
        raise info 'sal:%',a.sal;
        raise info '%',mycursor%rowcount;
    end if;
    if  mycursor%isopen then
        raise info 'mycursor is open';
        close mycursor;
    end if;
end;
/
call syscur_002();
drop table emp;
drop procedure syscur_002;