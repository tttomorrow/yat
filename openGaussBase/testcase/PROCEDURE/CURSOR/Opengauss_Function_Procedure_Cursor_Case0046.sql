-- @testpoint: 给游标变量赋空值null ,'',' '

drop table if exists emp_test;
create table emp_test(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp_test values(1,'zhangsan','doctor1',10000);
insert into emp_test values(2,'zhangsan2','doctor2',10000);
insert into emp_test values(123,'zhangsan3','doctor3',10000);
insert into emp_test values(1,'zhansi','doctor1',12000);
insert into emp_test values(2,'lisiabc','doctor2',13000);
insert into emp_test values(123,'zhangwu123','doctor3',14000);

create or replace procedure syscur_046()
is
declare
   cv SYS_REFCURSOR;
   v_ename varchar2(20);
begin
    open cv for select null from sys_dummy;
    loop
    fetch cv into v_ename;
        exit when cv%notfound;
        raise info 'the results is%',v_ename;
        raise info 'row count is% ',cv%rowcount;
    end loop;
    close cv;
end;
/
call syscur_046();
drop procedure syscur_046;


create or replace procedure syscur_046()
is
declare
   cv SYS_REFCURSOR;
   v_ename varchar2(20);
begin
    open cv for select '' from sys_dummy;
    loop
    fetch cv into v_ename;
        exit when cv%notfound;
        raise info 'the results is% ',v_ename;
        raise info 'row count is% ',cv%rowcount;
    end loop;
    close cv;
end;
/
call syscur_046();
drop procedure syscur_046;

create or replace procedure syscur_046()
is
declare
   cv SYS_REFCURSOR;
   v_ename varchar2(20);
begin
    open cv for select ' ' from sys_dummy;
    loop
        fetch cv into v_ename;
        exit when cv%notfound;
        raise info 'the results is% ',v_ename;
        raise info 'row count is% ',cv%rowcount;
    end loop;
    close cv;
end;
/
call syscur_046();
drop procedure syscur_046;
drop table emp_test;