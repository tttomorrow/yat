-- @testpoint: 存储过程中嵌套游标并多次打开和关闭同一个游标

drop table if exists emp_test;
create table emp_test(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp_test values(1,'zhangsan','doctor1',10000);
insert into emp_test values(2,'zhangsan2','doctor2',10000);
insert into emp_test values(123,'zhangsan3','doctor3',10000);
insert into emp_test values(1,'zhansi','doctor1',12000);
insert into emp_test values(2,'lisiabc','doctor2',13000);
insert into emp_test values(123,'zhangwu123','doctor3',14000);

create or replace procedure syscur_049(v_num int)
as
	cv SYS_REFCURSor;
	v_empno NUMBER(10,0);
        v_empno1 int;
begin
	select count(*) into v_empno from emp_test;
	if v_empno <> v_num then
	    open cv for select 1 from sys_dummy;
        fetch cv into v_empno1;
        raise info ':%',v_empno1;
        close cv;
	else
		open cv for select 0 from sys_dummy;
        fetch cv into v_empno1;
        raise info ':%',v_empno1;
        close cv;
	end if;
end;
/
call syscur_049(3);
call syscur_049(6);
drop procedure syscur_049;