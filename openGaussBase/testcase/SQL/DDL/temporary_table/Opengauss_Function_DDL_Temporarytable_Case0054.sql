-- @testpoint: 创建列存临时表
-- @modify at: 2020-11-24
drop table if exists temp_table_054;
create  temporary table temp_table_054(a int,b int,c int)WITH (ORIENTATION = COLUMN);
--插入数据
insert into temp_table_054 values(1,2,3);
insert into temp_table_054 values(11,22,33);
insert into temp_table_054 values(111,222,333);
--查询
select * from temp_table_054;
--删表
drop table temp_table_054;