-- @testpoint: 自定义函数blob数据类型的测试———自定义函数内的blob类型和binary类型的转换 合理报错，不支持binary类型

drop table if exists fvt_func_blob_table_006;
create table fvt_func_blob_table_006(
  t1 int,
  t2 blob
  );
insert into fvt_func_blob_table_006 values(1,'01010101111100000100000010000000100111111111');

--创建自定义函数
create or replace function fvt_func_blob_006() return binary
is
v1 binary(200);
begin
  select t2 into v1 from fvt_func_blob_table_006 where t1=1;
  insert into fvt_func_blob_table_006 values(vsize(v1),v1);
  return v1;
  exception
  when no_data_found
  then
raise info 'no_data_found';
end;
/
--调用自定义函数
select fvt_func_blob_006();

select * from fvt_func_blob_table_006 where t1!=1;

--恢复环境
drop function if exists fvt_func_blob_006;
drop table if exists fvt_func_blob_table_006;

