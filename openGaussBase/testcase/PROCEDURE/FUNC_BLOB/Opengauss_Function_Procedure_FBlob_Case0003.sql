-- @testpoint: 自定义函数blob数据类型的测试

drop table if exists fvt_proc_binary_blob_003;
create table fvt_proc_binary_blob_003(
  t1 int,
  t2 blob
  );
insert into fvt_proc_binary_blob_003 values(1,'0101101111');

create or replace function fvt_proc_blob_003() return int
is
v1 blob;
v2 int;
begin
  select t2 into v1 from fvt_proc_binary_blob_003 where t1=1;
    raise info 'v2=%',v2;
    return v1;
  exception
  when
    no_data_found
  then
    raise info 'no_data_found';
end;
/
--调用自定义函数
select fvt_proc_blob_003();

--恢复环境
drop function if exists fvt_proc_blob_003;
drop table if exists fvt_proc_binary_blob_003;


