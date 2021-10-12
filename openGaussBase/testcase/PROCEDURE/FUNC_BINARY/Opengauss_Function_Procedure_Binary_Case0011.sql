-- @testpoint: BINARY类型的测试———测试RAW类型和BLOB的转换

drop table if exists FVT_FUNC_BINARY_TABLE_011;
create table FVT_FUNC_BINARY_TABLE_011(T1 INT,T2 RAW(100));

--创建自定义函数
create or replace function FVT_FUNC_BINARY_011() return RAW
is
V1 FVT_FUNC_BINARY_TABLE_011.T2%TYPE;
begin
  select T2 into V1 from FVT_FUNC_BINARY_TABLE_011 where T1=1;
  return V1;
  EXCEPTION
WHEN NO_DATA_FOUND THEN  raise info 'NO_DATA_FOUND';
end;
/
--调用自定义函数
select FVT_FUNC_BINARY_011();

--修改列属性
--增加临时列
alter table FVT_FUNC_BINARY_TABLE_011 add T3 RAW(100);
--把数据放到临时列，置空数据列
update FVT_FUNC_BINARY_TABLE_011 set T3=T2 ,T2=null;
--修改字段类型
alter table FVT_FUNC_BINARY_TABLE_011 modify T2 BLOB;
--放回数据
update FVT_FUNC_BINARY_TABLE_011 set T2=T3 where T3 is not null;
--删除临时列
alter table FVT_FUNC_BINARY_TABLE_011 drop column T3;

--调用自定义函数
select FVT_FUNC_BINARY_011();

--恢复环境
drop table if exists FVT_FUNC_BINARY_TABLE_011;
drop function if exists FVT_FUNC_BINARY_011;

