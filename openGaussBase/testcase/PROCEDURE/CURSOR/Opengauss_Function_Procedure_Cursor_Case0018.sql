-- @testpoint: 显示游标作为out参数使用 合理报错

drop table if exists emp;
create table emp(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp values(1,'zhangsan','doctor1',10000),(2,'zhangsan2','doctor2',10000),(123,'zhangsan3','doctor3',10000);
insert into emp values(1,'zhansi','doctor1',10000),(2,'lisiabc','doctor2',10000),(123,'zhangwu123','doctor3',10000);
insert into emp values(10,'abc','worker',9000);
insert into emp values(716,'ZHANGSAN','leader',20000);

create or replace procedure syscur_018(sys_cur out cursor)
    is
    cursor C1 is select empno,ename from emp  where empno=1 order by empno;
begin
    open C1;
    sys_cur := C1;
end;
/
call syscur_018();
drop table emp;
drop procedure syscur_018;