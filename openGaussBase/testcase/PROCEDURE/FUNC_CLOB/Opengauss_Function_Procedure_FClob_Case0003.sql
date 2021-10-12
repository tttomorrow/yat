-- @testpoint: 自定义函数CLOB数据类型的测试

drop table if exists FVT_FUNC_CLOB_TABLE_003;
create table FVT_FUNC_CLOB_TABLE_003(
  T1 INT,
  T2 TEXT
  );

--创建自定义函数
create or replace function FVT_FUNC_CLOB_003() return char
is
V1 clob;
begin
  select T2 into V1 from FVT_FUNC_CLOB_TABLE_003 where T1=1;
  return V1;
  EXCEPTION
  WHEN
    NO_DATA_FOUND
  THEN
    raise info 'NO_DATA_FOUND';
end;
/
--调用自定义函数
select FVT_FUNC_CLOB_003();

--恢复环境
DROP function if exists FVT_FUNC_CLOB_003;
drop table if exists fvt_func_clob_table_003;