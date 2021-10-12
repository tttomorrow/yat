-- @testpoint: 创建存储过程时带shippable参数

create table test_emp_001(name varchar(10));
--创建存储过程带参数shippable
create or replace procedure test_proc_using_008() shippable as
  v_sql varchar2(2000);
begin
    v_sql := 'insert into test_emp_001 values (:v1)';
    execute immediate v_sql using  'kimy';
end;
/
--调用存储过程
call test_proc_using_008();

--查看表结构
select * from test_emp_001;

--清理环境
drop procedure test_proc_using_008;
drop table test_emp_001;


create table test_emp_001(name varchar(10));
--创建存储过程不带参数shippable
create or replace procedure test_proc_using_008() as
  v_sql varchar2(2000);
begin
    v_sql := 'insert into test_emp_001 values (:v1)';
    execute immediate v_sql using  'kimy';
end;
/
--调用存储过程
call test_proc_using_008();

--查看表结构
select * from test_emp_001;

--清理环境
drop procedure test_proc_using_008;
drop table test_emp_001;