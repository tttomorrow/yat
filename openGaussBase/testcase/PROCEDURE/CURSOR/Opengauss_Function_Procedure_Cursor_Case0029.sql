-- @testpoint: 存储过程中游标使用 存储过程中使用for游标，if…调用正常

drop table if exists emp;
create table emp(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp values(1,'zhangsan','doctor1',10000),(2,'zhangsan2','doctor2',10000),(123,'zhangsan3','doctor3',10000);
insert into emp values(1,'zhansi','doctor1',10000),(2,'lisiabc','doctor2',10000),(123,'zhangwu123','doctor3',10000);
insert into emp values(10,'abc','worker',9000);
insert into emp values(716,'ZHANGSAN','leader',20000);

create or  replace procedure syscur_029(a int) is
    cursor mycursor is select * from emp where empno != 123 and sal=10000;
    b emp%rowtype;
    mysyscur  sys_refcursor;
    strSQL1 varchar(1000);
    strSQL2 varchar(1000);
begin
    strSQL1 := 'select * from emp  where  sal <> 10000';
    strSQL2 := '';
    if a <= 10 then
    for i in mycursor
        loop
        raise info ' is not 10000:%',i.ename;
        end loop;
    elsif a >10 and a <100 then
        open mysyscur for  strSQL1;
        fetch mysyscur into  b;
        raise info ' a > 10 and a < 100:%',b.ename;
        close mysyscur;
    else
        open mysyscur for strSQL2;
        raise info 'else a > 10 and a < 100';
    end if;
end;
/
--调用成功
call syscur_029(10);
drop table emp;
drop procedure syscur_029;
