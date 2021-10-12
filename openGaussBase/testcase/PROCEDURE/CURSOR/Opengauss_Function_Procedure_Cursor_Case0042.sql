-- @testpoint: 游标变量指定的sql嵌套lpad函数和trunc函数

drop table if exists emp_test;
create table emp_test(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp_test values(1,'zhangsan','doctor1',10000);
insert into emp_test values(2,'zhangsan2','doctor2',10000);
insert into emp_test values(123,'zhangsan3','doctor3',10000);
insert into emp_test values(1,'zhansi','doctor1',12000);
insert into emp_test values(2,'lisiabc','doctor2',13000);
insert into emp_test values(123,'zhangwu123','doctor3',14000);

create or replace procedure syscur_042()
is
declare
   cv SYS_REFCURSor;
   v_sal emp_test.sal%type;
   v_ename  varchar(20);
begin
    open cv for select lpad(ename,15,job),trunc(sal,-4)*3 from emp_test where ename like 'zh%' order by job,ename;
    loop
    fetch cv into v_ename,v_sal;
        exit when cv%notfound;
        raise info 'name is%',v_ename;
        raise info 'salary is% ',v_sal;
    end loop;
end;
/
call syscur_042();
drop table emp_test;
drop procedure syscur_042;
