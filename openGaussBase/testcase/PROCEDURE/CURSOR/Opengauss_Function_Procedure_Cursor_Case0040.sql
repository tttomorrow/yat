-- @testpoint: 游标变量指定的sql语句带可变参数

drop table if exists emp_test;
create table emp_test(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp_test values(1,'zhangsan','doctor1',10000);
insert into emp_test values(2,'zhangsan2','doctor2',10000);
insert into emp_test values(123,'zhangsan3','doctor3',10000);
insert into emp_test values(1,'zhansi','doctor1',12000);
insert into emp_test values(2,'lisiabc','doctor2',13000);
insert into emp_test values(123,'zhangwu123','doctor3',14000);

create or replace procedure syscur_040()
is
DECLARE
  cv SYS_REFCURSor;
  v_sal   emp_test.sal%type;
  v_sal_mul     emp_test.sal%type;
  factor   integer :=2;
begin
    open cv for select sal,sal*factor from emp_test where job like '%1' and sal < 13000 order by sal;
    loop
    fetch cv into v_sal,v_sal_mul;
    exit when cv%notfound;
        raise info 'factor =%',factor;
        raise info 'sal =%',v_sal;
        raise info 'sal_mul =%',v_sal_mul;
        factor := factor+1;
    end loop;
    close cv;
end;
/
call syscur_040();
drop procedure syscur_040;
drop table emp_test;