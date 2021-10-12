-- @testpoint: 游标绑定的select带有union后带where子句

drop table if exists emp;
create table emp(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp values(1,'zhangsan','doctor1',10000),(2,'zhangsan2','doctor2',10000),(123,'zhangsan3','doctor3',10000);
insert into emp values(1,'zhansi','doctor1',10000),(2,'lisiabc','doctor2',10000),(123,'zhangwu123','doctor3',10000);
insert into emp values(10,'abc','worker',9000);
insert into emp values(716,'ZHANGSAN','leader',20000);

drop table if exists emp2;
create table emp2(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp2 values(1,'zhangsan','doctor1',100),(2,'zhangsan2','doctor2',10000),(123,'zhangsan3','doctor3',10000);

create or replace procedure syscur_017()
is
declare
    cursor mycursor  is select * from emp union select * from emp2  where  ename like '%zhangsan%' and sal > 9000 order by empno,ename,job ;
begin
    for a  in  mycursor
    loop
        raise info 'a is emp:%',a.ENAME;
        raise info 'user$ name is:%',a.job;
        raise info ':%',mycursor%rowcount;
    end loop;
end;
/
call syscur_017();
drop table emp;
drop table emp2;
drop procedure syscur_017;
