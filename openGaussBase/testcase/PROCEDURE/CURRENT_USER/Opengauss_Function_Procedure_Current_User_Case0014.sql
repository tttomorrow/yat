-- @testpoint: 创建存储过程时带 returns null on null input 参数

create table test_emp_001(name varchar(10));
create or replace procedure test_proc_using_014(a int) returns null on null input as
  v_sql varchar2(2000);
begin
    v_sql := 'insert into test_emp_001 values (:v1)';
    execute immediate v_sql using  'kimy';
end;
/
--调用存储过程时带null参数
call test_proc_using_014(null);

--查看表结构 没有数据
select * from test_emp_001;

--正常调用存储过程
call test_proc_using_014(1);
--查看表结构 数据插入成功
select * from test_emp_001;

--清理环境
drop procedure test_proc_using_014;
drop table test_emp_001;

--创建存储过程时不带 returns null on null input 参数
create table test_emp_001(name varchar(10));
create or replace procedure test_proc_using_014(a int) as
  v_sql varchar2(2000);
begin
    v_sql := 'insert into test_emp_001 values (:v1)';
    execute immediate v_sql using  'kimy';
end;
/
--调用存储过程时带null参数
call test_proc_using_014(null);

--查看表结构 数据插入成功
select * from test_emp_001;

--清理环境
drop procedure test_proc_using_014;
drop table test_emp_001;