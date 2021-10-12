-- @testpoint: 创建存储过程时带volatile参数

--创建存储过程时带volatile参数
drop table if exists test_emp_001;
create table test_emp_001(name varchar(10));
create or replace procedure test_proc_using_007() volatile as
  v_sql varchar2(2000);
begin
    v_sql := 'insert into test_emp_001 values (:v1)';
    execute immediate v_sql using  'kimy';
end;
/
--调用存储过程
call test_proc_using_007();

--查看表结构
select name from test_emp_001;

--清理环境
drop procedure test_proc_using_007;
drop table test_emp_001;

--创建存储过程时不带volatile参数
drop table if exists test_emp_001;
create table test_emp_001(name varchar(10));
create or replace procedure test_proc_using_007() as
  v_sql varchar2(2000);
begin
    v_sql := 'insert into test_emp_001 values (:v1)';
    execute immediate v_sql using  'kimy';
end;
/
--调用存储过程
call test_proc_using_007();

--查看表结构
select name from test_emp_001;

--清理环境
drop procedure test_proc_using_007;
drop table test_emp_001;
