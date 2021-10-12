-- @testpoint: 字符串作为游标的输入

drop table if exists emp_test;
create table emp_test(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp_test values(1,'zhangsan','doctor1',10000);
insert into emp_test values(2,'zhangsan2','doctor2',10000);
insert into emp_test values(123,'zhangsan3','doctor3',10000);
insert into emp_test values(1,'zhansi','doctor1',12000);
insert into emp_test values(2,'lisiabc','doctor2',13000);
insert into emp_test values(123,'zhangwu123','doctor3',14000);

create or replace procedure syscur_039()
is
declare
  cv SYS_REFCURSor;
  v_emp_test   emp_test%rowtype;
  query_2 varchar(200) :='select * from emp_test where sal in (10000,12000) order by sal,ename';
begin
    open cv for query_2;
    fetch cv into v_emp_test;
    while cv%found loop
        raise info '% ',v_emp_test.sal;
        fetch cv into v_emp_test;
    end loop;
    close cv;
end;
/
call syscur_039();
drop procedure syscur_039;
drop table emp_test;

