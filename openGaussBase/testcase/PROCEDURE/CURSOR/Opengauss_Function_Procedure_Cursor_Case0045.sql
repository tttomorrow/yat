-- @testpoint: 存储过程中带游标变量

drop table if exists emp_test;
create table emp_test(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp_test values(1,'zhangsan','doctor1',10000);
insert into emp_test values(2,'zhangsan2','doctor2',10000);
insert into emp_test values(123,'zhangsan3','doctor3',10000);
insert into emp_test values(1,'zhansi','doctor1',12000);
insert into emp_test values(2,'lisiabc','doctor2',13000);
insert into emp_test values(123,'zhangwu123','doctor3',14000);

create or replace procedure syscur_045(cur_num int)
is
   cv SYS_REFCURSOR;
   v_ename  emp_test.ename%type;
begin
    open cv for select ename from emp_test where empno=cur_num order by ename;
    loop
        fetch cv into v_ename;
        exit when cv%notfound;
        raise info 'ename is %',v_ename;
    end loop;
    close cv;
end;
/
call syscur_045(123);
drop table emp_test;
drop procedure syscur_045;
