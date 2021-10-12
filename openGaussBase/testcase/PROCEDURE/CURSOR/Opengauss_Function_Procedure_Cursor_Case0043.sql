-- @testpoint: 游标变量指定的sql嵌套sum和avg函数

drop table if exists emp_test;
create table emp_test(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp_test values(1,'zhangsan','doctor1',10000);
insert into emp_test values(2,'zhangsan2','doctor2',10000);
insert into emp_test values(123,'zhangsan3','doctor3',10000);
insert into emp_test values(1,'zhansi','doctor1',12000);
insert into emp_test values(2,'lisiabc','doctor2',13000);
insert into emp_test values(123,'zhangwu123','doctor3',14000);

create or replace procedure syscur_043()
is
declare
   cv SYS_REFCURSor;
   v_sum  int;
   v_avg  int;
   v_empno emp_test.empno%type;
begin
    open cv for select empno,sum(sal),avg(sal) from emp_test group by empno,job order by empno;
    loop
    fetch cv into v_empno,v_sum,v_avg;
        exit when cv%notfound;
        raise info 'sum is% ',v_sum;
        raise info 'avg is% ',v_avg;
    end loop;
    close cv;
end;
/
call syscur_043();
drop table emp_test;
drop procedure syscur_043;
