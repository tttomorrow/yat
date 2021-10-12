-- @testpoint: 创建全局临时表，添加if not exists参数
-- @modify at: 2020-11-24
--建表
create global temporary table if not exists temp_table_055(
  t1 int,
  t2 blob
  );
--再次创建同名表，不会报错
create global temporary table if not exists temp_table_055(
  t1 int,
  t2 blob
  );
--查询
select * from temp_table_055;
--删表
drop table temp_table_055;

