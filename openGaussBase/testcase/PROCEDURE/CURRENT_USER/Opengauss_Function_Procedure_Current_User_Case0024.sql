-- @testpoint: 设置数据库的会话参数值为 default ,使用to

create table test_emp_001(name varchar(10));
create or replace procedure test_proc_using_001() set current_schema to default as
  v_sql varchar2(2000);
begin
    v_sql := 'insert into test_emp_001 values (:v1)';
    execute immediate v_sql using  'kimy';
end;
/
--调用存储过程
call test_proc_using_001();

--查看表结构
select * from test_emp_001;

--清理环境
drop procedure test_proc_using_001;
drop table test_emp_001;
