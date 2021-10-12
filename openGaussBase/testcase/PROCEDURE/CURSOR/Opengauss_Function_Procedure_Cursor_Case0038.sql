-- @testpoint: 显示游标和游标变量的综合使用

drop table if exists emp_test;
create table emp_test(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp_test values(1,'zhangsan','doctor1',10000);
insert into emp_test values(2,'zhangsan2','doctor2',10000);
insert into emp_test values(123,'zhangsan3','doctor3',10000);
insert into emp_test values(1,'zhansi','doctor1',12000);
insert into emp_test values(2,'lisiabc','doctor2',13000);
insert into emp_test values(123,'zhangwu123','doctor3',14000);

drop table if exists  syscur_038;
create table syscur_038(cur_num int,cur_name varchar(10));

declare
  cv SYS_REFCURSOR;
  v_ename   emp_test.ename%TYPE;
  v_empno   emp_test.empno%type;
  cursor cursor_1 is select empno from emp_test order by empno;
begin
  open cursor_1;
  fetch cursor_1 into v_empno;
  while cursor_1%found loop
 	 open cv for select ename from emp_test where empno=v_empno;
     fetch cv into v_ename;
     while cv%found loop
        fetch cv into v_ename;
     end loop;
     insert into syscur_038 values(v_empno,v_ename);
     close cv;
  fetch cursor_1 into v_empno;
  end loop;
  close cursor_1;
  end;
/
select * from syscur_038 order by cur_num;
drop table emp_test;
drop table syscur_038;
