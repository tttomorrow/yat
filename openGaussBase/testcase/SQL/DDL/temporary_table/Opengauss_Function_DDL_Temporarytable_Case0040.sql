-- @testpoint: 创建字段名中有汉字的临时表
-- @modify at: 2020-11-24
--建表
drop table if exists temp_table_040;
create temporary table temp_table_040(万 int);
--删表
drop table temp_table_040;


