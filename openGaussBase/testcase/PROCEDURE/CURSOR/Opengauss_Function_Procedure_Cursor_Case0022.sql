-- @testpoint: 普通变量varchar%type

drop table if exists emp;
create table emp(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp values(1,'zhangsan','doctor1',10000),(2,'zhangsan2','doctor2',10000),(123,'zhangsan3','doctor3',10000);
insert into emp values(1,'zhansi','doctor1',10000),(2,'lisiabc','doctor2',10000),(123,'zhangwu123','doctor3',10000);
insert into emp values(10,'abc','worker',9000);
insert into emp values(716,'ZHANGSAN','leader',20000);

create or replace procedure syscur_022()
is
declare
    a varchar(20);
    b a%type;
    c1 sys_refcursor;
begin
    open c1 for select ename from emp;
    fetch c1 into b;
    raise info 'result is:%',b;
    fetch c1 into b;
    raise info 'result is:%', b;
    close c1;
end;
/
call syscur_022();
drop table emp;
drop procedure syscur_022;
