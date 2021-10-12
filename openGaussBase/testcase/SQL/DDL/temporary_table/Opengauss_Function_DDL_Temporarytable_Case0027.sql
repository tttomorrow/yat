-- @testpoint: 删除带参数on commit delete rows的全局临时表
-- @modify at: 2020-11-24
--建表
drop table if exists temp_table_027;
create global temporary table temp_table_027(
  t1 int,
  t2 clob
  )on commit delete rows;
--插入数据
insert into temp_table_027 values (1,'0101010');
--查询表，无数据
select * from temp_table_027;
--删表
drop table temp_table_027;

