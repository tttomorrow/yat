-- @testpoint: 创建循环游标

drop table if exists emp_test;
create table emp_test(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp_test values(1,'zhangsan','doctor1',10000);
insert into emp_test values(2,'zhangsan2','doctor2',10000);
insert into emp_test values(123,'zhangsan3','doctor3',10000);
insert into emp_test values(1,'zhansi','doctor1',12000);
insert into emp_test values(2,'lisiabc','doctor2',13000);
insert into emp_test values(123,'zhangwu123','doctor3',14000);

create or replace procedure syscur_037()
is
declare
  v_emp_test     emp_test%ROWTYPE;
  cursor cv is select * from emp_test order by empno,ename;
begin
 for v_emp_test in cv
    loop
    raise info '% ',v_emp_test.ename;
    end loop;
   raise info  '-------------------------------------';
end;
/
call syscur_037();
drop procedure syscur_037;
drop table emp_test;