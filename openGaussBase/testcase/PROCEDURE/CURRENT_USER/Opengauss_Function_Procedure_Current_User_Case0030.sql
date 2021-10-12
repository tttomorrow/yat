-- @testpoint: 创建存储过程时各参数综合使用

create table test_emp_001(name varchar(10));
create or replace procedure test_proc_using_001(a int) SHIPPABLE  LEAKPROOF CALLED ON NULL INPUT  external security invoker cost 0.000056  as
  v_sql varchar2(2000);
begin
    v_sql := 'insert into test_emp_001 values (:v1)';
    execute immediate v_sql using  'kimy';
end;
/
--调用存储过程
call test_proc_using_001(null);

--查看表结构
select * from test_emp_001;

--调用存储过程
call test_proc_using_001(1);

--查看表结构
select * from test_emp_001;

--清理环境
drop procedure test_proc_using_001;
drop table test_emp_001;
