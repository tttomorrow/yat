-- @testpoint: 创建存储过程时参数模式和参数名称顺序调换 参数顺序为：参数模式、参数数据类型、参数名 合理报错

-- 创建存储过程时参数模式在前，参数名称在后
create table test_emp_001(name varchar(10));
create or replace procedure test_proc_using_001(in a int ) as
  v_sql varchar2(2000);
begin
    v_sql := 'insert into test_emp_001 values (:v1)';
    execute immediate v_sql using  'kimy';
end;
/
--调用存储过程
call test_proc_using_001(1);

--查看表结构
select * from test_emp_001;

--清理环境
drop procedure test_proc_using_001;
drop table test_emp_001;


-- 创建存储过程时参数顺序为：参数模式、参数数据类型、参数名 合理报错
create table test_emp_001(name varchar(10));
create or replace procedure test_proc_using_001(in int a) as
  v_sql varchar2(2000);
begin
    v_sql := 'insert into test_emp_001 values (:v1)';
    execute immediate v_sql using  'kimy';
end;
/
--调用存储过程
call test_proc_using_001(1);

--查看表结构
select * from test_emp_001;

--清理环境
drop procedure test_proc_using_001;
drop table test_emp_001;