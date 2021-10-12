-- @testpoint: 存储过程中游标使用for变量循环

drop table if exists emp;
create table emp(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp values(1,'zhangsan','doctor1',10000),(2,'zhangsan2','doctor2',10000),(123,'zhangsan3','doctor3',10000);
insert into emp values(1,'zhansi','doctor1',10000),(2,'lisiabc','doctor2',10000),(123,'zhangwu123','doctor3',10000);
insert into emp values(10,'abc','worker',9000);
insert into emp values(716,'ZHANGSAN','leader',20000);

create or replace procedure syscur_014()
is
declare
    cursor mycursor  is select * from emp where ename like '%zhangsan%' and sal > 9000 order by empno;
begin
    for a  in  mycursor
    loop
        raise info 'a is emp:%',a.empno;
        raise info 'name:%',a.ename;
        raise info 'job:%',a.job;
        raise info 'sal:%',a.sal;
        raise info ':%',mycursor%rowcount;
    end loop;
end;
/
call syscur_014();
drop table emp;
drop procedure syscur_014;