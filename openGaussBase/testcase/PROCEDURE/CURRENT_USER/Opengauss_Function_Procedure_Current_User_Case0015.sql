-- @testpoint: 创建存储过程时带strict参数--returns null on null input和strict的功能相同，指定如果函数的某个参数是null，此函数总是返回null

create table test_emp_001(name varchar(10));
create or replace procedure test_proc_using_015(a int) strict as
  v_sql varchar2(2000);
begin
    v_sql := 'insert into test_emp_001 values (:v1)';
    execute immediate v_sql using  'kimy';
end;
/
--调用存储过程时带null参数
call test_proc_using_015(null);
--查看表结构 没有数据
select * from test_emp_001;

--正常调用存储过程
call test_proc_using_015(1);
--查看表结构 数据插入成功
select * from test_emp_001;

--清理环境
drop procedure test_proc_using_015;
drop table test_emp_001;

--创建存储过程时不带 strict 参数
create table test_emp_001(name varchar(10));
create or replace procedure test_proc_using_015(a int) as
  v_sql varchar2(2000);
begin
    v_sql := 'insert into test_emp_001 values (:v1)';
    execute immediate v_sql using  'kimy';
end;
/
--调用存储过程时带null参数
call test_proc_using_015(null);

--查看表结构 数据插入成功
select * from test_emp_001;

--清理环境
drop procedure test_proc_using_015;
drop table test_emp_001;