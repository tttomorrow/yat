-- @testpoint: 隐式游标%isopen总是false

drop table if exists emp_test;
create table emp_test(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp_test values(1,'zhangsan','doctor1',10000);
insert into emp_test values(2,'zhangsan2','doctor2',10000);
insert into emp_test values(123,'zhangsan3','doctor3',10000);
insert into emp_test values(1,'zhansi','doctor1',12000);
insert into emp_test values(2,'lisiabc','doctor2',13000);
insert into emp_test values(123,'zhangwu123','doctor3',14000);

create or replace procedure syscur_047()
is
declare
v_empno  emp_test.empno%type;
v_ename  emp_test.ename%type;
begin
    select empno,ename into v_empno,v_ename from emp_test where ename='zhangsan';
    if not sql%isopen then
        raise info 'cursor is open';
    end if;
    if sql%found then
        raise info 'number is% ',v_empno;
        raise info 'name is%',v_ename;
    end if;
end;
/
call syscur_047();
drop procedure syscur_047;
drop table emp_test;