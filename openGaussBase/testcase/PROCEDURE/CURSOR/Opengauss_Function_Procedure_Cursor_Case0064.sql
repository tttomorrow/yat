-- @testpoint: 带参数游标，指定参数类型，无默认值，一次fetch多个字段列到不同变量，select子表达式含游标参数

drop table if exists emp;
create table emp(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp values(1,'zhangsan','doctor1',10000),(2,'zhangsan2','doctor2',10001),(3,'zhangsan3','doctor3',10002);
insert into emp values(1,'zhansi','doctor1',10003),(2,'lisiabc','doctor2',10004),(3,'zhangwu123','doctor3',10005);

create or replace procedure p_emp_012(str boolean)
as
declare
    cursor mycursor(job_real varchar2,max_sal number ) is  select empno,ename,(sal-max_sal) overpament from emp where job=job_real and sal> max_sal  order by sal,ename;
    c_empno emp.empno%type;
    c_ename emp.ename%type;
    c_overpament emp.sal%type;
begin
    open mycursor('doctor1',9000);
    fetch mycursor into c_empno,c_ename,c_overpament;
    loop
    if  mycursor%found then
        update emp set job='teacher' where empno=3;
        fetch mycursor into c_empno,c_ename,c_overpament;
        raise info'mycursor:%',mycursor;
    else
    exit;
    end if;
    end loop;
    close mycursor;
end;
/

 call p_emp_012(true);
 drop procedure p_emp_012;