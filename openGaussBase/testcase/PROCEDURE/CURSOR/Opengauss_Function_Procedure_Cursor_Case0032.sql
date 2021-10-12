-- @testpoint: 存储过程结合case when调用游标select exists(select)语句

drop table if exists emp;
create table emp(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp values(1,'zhangsan','doctor1',10000),(2,'zhangsan2','doctor2',10000),(123,'zhangsan3','doctor3',10000);
insert into emp values(1,'zhansi','doctor1',10000),(2,'lisiabc','doctor2',10000),(123,'zhangwu123','doctor3',10000);
insert into emp values(10,'abc','worker',9000);
insert into emp values(716,'ZHANGSAN','leader',20000);

drop table if exists emp2;
create table emp2(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp2 values(1,'zhangsan','doctor1',100),(2,'zhangsan2','doctor2',10000),(123,'zhangsan3','doctor3',10000);

create or replace procedure syscur_032(selected char) as
    cursor mycursor is   select * from emp where exists (select * from emp2 where emp2.ename=emp.ename);
begin
    case selected
    when 'A' then raise info 'select A';
    for i in mycursor loop
        raise info ':%',i.ename;
        raise info ':%',i.empno;
    end loop;
    when 'B' then raise info 'select B';
    else  raise info 'nosuch selected';
    end case;
end;
/
call syscur_032('A');
call syscur_032('B');
call syscur_032('1');
drop table emp;
drop table emp2;
drop procedure syscur_032;