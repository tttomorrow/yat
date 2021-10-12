-- @testpoint: 游标变量指定的sql语句带子查询
drop table if exists syscur_041;
create table syscur_041(empno int,edepart varchar(20));
insert into syscur_041 values(1,'jizhenshi');
insert into syscur_041 values(2,'guke');
insert into syscur_041 values(3,'xueyeke');

drop table if exists emp_test;
create table emp_test(empno int,ename varchar(10),job varchar(10) ,sal integer);
insert into emp_test values(1,'zhangsan','doctor1',10000);
insert into emp_test values(2,'zhangsan2','doctor2',10000);
insert into emp_test values(123,'zhangsan3','doctor3',10000);
insert into emp_test values(1,'zhansi','doctor1',12000);
insert into emp_test values(2,'lisiabc','doctor2',13000);
insert into emp_test values(123,'zhangwu123','doctor3',14000);

create or replace procedure syscur_041()
is
declare
   cv SYS_REFCURSor;
   v_emptest emp_test%rowtype;
begin
    open cv for select * from emp_test where empno=(select empno from syscur_041 where edepart='guke') and job like '%d%' order by empno,ename;
    loop
        fetch cv into v_emptest;
        exit when cv%notfound;
        raise info 'v_emptest.ename =%',v_emptest.ename;
    end loop;
end;
/
call syscur_041();
drop table emp_test;
drop table syscur_041;
drop procedure syscur_041;
