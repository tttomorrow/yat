-- @testpoint: 带参数游标，指定参数类型，无默认值，一次fetch多个字段列到不同变量，select子表达式含游标参数

drop table if exists emp;
create table emp(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp values(1,'zhangsan','doctor1',10000),(2,'zhangsan2','doctor2',10000),(123,'zhangsan3','doctor3',10000);
insert into emp values(1,'zhansi','doctor1',10000),(2,'lisiabc','doctor2',10000),(123,'zhangwu123','doctor3',10000);
insert into emp values(10,'abc','worker',9000);
insert into emp values(716,'ZHANGSAN','leader',20000);

create or replace procedure syscur_012()
is
declare
    cursor mycursor(job_real varchar2,max_sal number ) is  select empno,ename,(sal-max_sal) overpament from emp where job=job_real and sal> max_sal  order by sal,ename;
    c_empno emp.empno%type;
    c_ename emp.ename%type;
    c_overpament emp.sal%type;
begin
    open mycursor('doctor1',9000);
    fetch mycursor into c_empno,c_ename,c_overpament;
    loop
    if  mycursor%found  then
        raise info 'a is emp:%',c_empno;
        raise info 'name:%',c_ename;
        raise info ':%',mycursor%rowcount;
    fetch mycursor into c_empno,c_ename,c_overpament;
    else
    exit;
    end if;
    end loop;
    close mycursor;
end;
/
call syscur_012();
drop table emp;
drop procedure syscur_012;