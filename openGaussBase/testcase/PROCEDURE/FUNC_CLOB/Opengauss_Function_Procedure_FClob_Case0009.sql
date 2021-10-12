-- @testpoint: 自定义函数CLOB数据类型的测试:结合to_char函数

--创建自定义函数
create or replace function fvt_func_clob_007(p1 in clob) return clob
is
begin
  return p1;
  exception
  when no_data_found
  then
    raise info 'no_data_found';
end;
/
--调用自定义函数
select FVT_FUNC_CLOB_007(to_char(88877));

--恢复环境
drop function fvt_func_clob_007;
