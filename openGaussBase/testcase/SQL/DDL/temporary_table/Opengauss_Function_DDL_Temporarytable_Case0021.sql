-- @testpoint: 删除本地临时表,语法错误，合理报错
-- @modify at: 2020-11-24
--建表
drop  table if exists temp_table_021;
create local temporary table temp_table_021(
  t1 int,
  t2 blob);
--插入数据
insert into temp_table_021 values (1,'0101010');
select * from temp_table_021;
--删除表，报错
drop  local temporary  table temp_table_021;
--删表
drop table if exists temp_table_021;
