-- @testpoint: 匿名块中游标使用%found

drop table if exists emp;
create table emp(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp values(1,'zhangsan','doctor1',10000),(2,'zhangsan2','doctor2',10000),(123,'zhangsan3','doctor3',10000);
insert into emp values(1,'zhansi','doctor1',10000),(2,'lisiabc','doctor2',10000),(123,'zhangwu123','doctor3',10000);
insert into emp values(10,'abc','worker',9000);
insert into emp values(716,'ZHANGSAN','leader',20000);

declare
    num number;
    begin
    update emp set empno=123 where empno=1;
if sql%found then
    raise info 'exists';
else
    raise info 'not exists';
end if;
end;
/
drop table emp;

