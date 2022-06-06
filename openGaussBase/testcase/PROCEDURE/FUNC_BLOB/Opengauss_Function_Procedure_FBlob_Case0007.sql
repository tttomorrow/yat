-- @testpoint: 自定义函数内的BLOB类型和RAW类型的转换

drop table if exists fvt_func_blob_table_007;
create table fvt_func_blob_table_007(
  t1 int,
  t2 blob
  );
insert into fvt_func_blob_table_007 values(1,'01010fadea0000001005678940111111111');

--创建自定义函数
create or replace function fvt_func_blob_007() return raw
is
v1 raw(200);
begin
  select t2 into v1 from fvt_func_blob_table_007 where t1=1;
  return v1;
  insert into fvt_func_blob_table_007 values(length(v1),v1);
  exception
  when no_data_found
  then
raise info 'no_data_found';
end;
/
--调用自定义函数
select fvt_func_blob_007();

--恢复环境
drop function if exists fvt_func_blob_007;
drop table if exists fvt_func_blob_table_007;


