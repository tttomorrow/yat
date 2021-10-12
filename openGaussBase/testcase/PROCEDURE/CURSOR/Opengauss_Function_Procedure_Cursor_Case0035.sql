-- @testpoint: 创建带游标变量的游标,测试游标属性%FOUND

drop table if exists emp_test;
create table emp_test(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp_test values(1,'zhangsan','doctor1',10000);
insert into emp_test values(2,'zhangsan2','doctor2',10000);
insert into emp_test values(123,'zhangsan3','doctor3',10000);
insert into emp_test values(1,'zhansi','doctor1',12000);
insert into emp_test values(2,'lisiabc','doctor2',13000);
insert into emp_test values(123,'zhangwu123','doctor3',14000);

create or replace procedure syscur_035()
is
DECLARE
  cv sys_refcursor;
  v_empno     emp_test.empno%TYPE;
  v_ename     emp_test.ename%TYPE;
begin
    open CV for select empno,ename from emp_test  where empno=1 order by empno,ename;
    fetch cv into v_empno, v_ename;
    while cv%FOUND loop
	raise info '% ',v_ename;
    fetch cv into v_empno, v_ename;
  end loop;
   raise info '-------------------------------------';
  close cv;
end;
/
call syscur_035();
drop procedure syscur_035;
drop table emp_test;