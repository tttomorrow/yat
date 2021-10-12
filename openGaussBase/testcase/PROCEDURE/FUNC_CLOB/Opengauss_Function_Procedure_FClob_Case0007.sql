-- @testpoint: 测试传入int/real类型

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
select fvt_func_clob_007(12);
select fvt_func_clob_007(12.256);

--恢复环境
drop function fvt_func_clob_007;
