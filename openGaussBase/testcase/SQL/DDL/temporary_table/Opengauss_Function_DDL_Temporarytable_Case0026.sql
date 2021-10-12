-- @testpoint: 删除临时表不带global/local temporary参数，删除成功
-- @modify at: 2020-11-24
--建表
drop  table if exists fvt_temp_table_001;
create   temporary table fvt_temp_table_001(
  t1 int,
  t2 blob);
--插入数据
insert into fvt_temp_table_001 values (1,'0101010');
select count(*) from fvt_temp_table_001;
--删表
drop table fvt_temp_table_001;