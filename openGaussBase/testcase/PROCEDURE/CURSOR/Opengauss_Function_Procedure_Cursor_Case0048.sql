-- @testpoint: 游标变量中的sql绑定select into语句 合理报错

drop table if exists emp_test;
create table emp_test(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp_test values(1,'zhangsan','doctor1',10000);
insert into emp_test values(2,'zhangsan2','doctor2',10000);
insert into emp_test values(123,'zhangsan3','doctor3',10000);
insert into emp_test values(1,'zhansi','doctor1',12000);
insert into emp_test values(2,'lisiabc','doctor2',13000);
insert into emp_test values(123,'zhangwu123','doctor3',14000);

create or replace procedure syscur_048()
is
declare
   cv SYS_REFCURSOR;
   v_ename varchar2(20);
   v_ename1 varchar2(20);
begin
    open cv for select ename into v_ename from emp_test where empno in(1,2) order by empno;
    loop
    fetch cv into v_ename1;
        exit when cv%notfound;
        raise info 'the results is %',v_ename1;
        raise info 'row count is % ',cv%rowcount;
    end loop;
    close cv;
end;
/
call syscur_048();
drop procedure syscur_048;
drop table emp_test;