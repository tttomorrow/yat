-- @testpoint: 临时表与自定义函数结合使用
-- @modify at: 2020-11-24
--建表并插入数据
drop table if exists temp_table_076;
create table temp_table_076 (a int);
insert into temp_table_076 values(1),(2);
--创建函数
CREATE OR REPLACE FUNCTION showall() RETURNS SETOF record
AS $$ SELECT count(*) from temp_table_076; $$
LANGUAGE SQL;
/
--调用函数，查询表的数据2行
select showall();
--删除函数
DROP FUNCTION showall();
--删除表
drop table temp_table_076;
