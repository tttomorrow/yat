-- @testpoint: blob作为type%类型

drop table if exists fvt_func_blob_table_002;
create table fvt_func_blob_table_002(
  t1 int,
  t2 blob
  );

--创建自定义函数
create or replace function fvt_func_blob_002() return blob
is
v1 blob:='01011';
v_lang fvt_func_blob_table_002.t2%type:='';
begin
  for i in 1 .. 99 loop
    v_lang := v_lang || '01011';
  end loop;
    return v_lang;
end;
/
--调用自定义函数
select fvt_func_blob_002();

--恢复环境
drop function if exists fvt_func_blob_002;
drop table if exists fvt_func_blob_table_002;