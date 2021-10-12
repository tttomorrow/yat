-- @testpoint: 创建有索引的临时表
-- @modify at: 2020-11-24
--建表
drop table if exists temp_table_049;
create  temporary table temp_table_049(a int,b char);
--建索引
drop index if exists index_tp ;
CREATE INDEX index_tp ON temp_table_049 (a);
--删表
drop table if exists temp_table_049 cascade;