-- @testpoint: 测试传入非字符串类型:bool,time

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
select FVT_FUNC_CLOB_007('true');
select FVT_FUNC_CLOB_007('0001-01-01 00:00:00');
select FVT_FUNC_CLOB_007('0001-01-01 00:00:00:0000');

--恢复环境
drop function fvt_func_clob_007;