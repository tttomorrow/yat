-- @testpoint: 游标中嵌套case when条件

drop table if exists emp_test;
create table emp_test(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp_test values(1,'zhangsan','doctor1',10000);
insert into emp_test values(2,'zhangsan2','doctor2',10000);
insert into emp_test values(123,'zhangsan3','doctor3',10000);
insert into emp_test values(1,'zhansi','doctor1',12000);
insert into emp_test values(2,'lisiabc','doctor2',13000);
insert into emp_test values(123,'zhangwu123','doctor3',14000);

create or replace procedure syscur_044()
is
declare
   cv SYS_REFCURSor;
   v_job emp_test.job%type;
   v_empno  emp_test.empno%type;
begin
    open cv for select distinct empno,job from emp_test group by empno,job order by 1,2;
    loop
        fetch cv into v_empno,v_job;
    exit when cv%notfound;
    case v_empno when 1 then
        raise info 'empno is %',v_empno;
        raise info 'job is %',v_job;
    when 2 then
        raise info 'empno is %',v_empno;
        raise info 'job is %',v_job;
    else
        raise info 'empno is %',v_empno;
        raise info 'job is %',v_job;
    end case;
    end loop;
    close cv;
end;
/
call syscur_044();
drop table emp_test;
drop procedure syscur_044;