-- @testpoint: 自定义函数BLOB数据类型的测试———非二进制类型 合理报错

--创建自定义函数
create or replace function FVT_FUNC_BINARY_008(P1 BLOB) return BLOB
is
begin
  return P1;
  EXCEPTION
  WHEN NO_DATA_FOUND
  THEN
raise info 'NO_DATA_FOUND';
end;
/
--调用自定义函数-int
select FVT_FUNC_BINARY_008(245);
--调用自定义函数-real
select FVT_FUNC_BINARY_008(245.1235);
--调用自定义函数-char
select FVT_FUNC_BINARY_008('ajkf*^&^&35GFFS');
--调用自定义函数-非法的十六进制字符串
select FVT_FUNC_BINARY_008(2XFA278FA);
--恢复环境
drop function if exists FVT_FUNC_BINARY_008;

