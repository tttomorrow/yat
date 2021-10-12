-- @testpoint: 修改字段值，字段与值的数据类型不匹配，合理报错
-- @modify at: 2020-11-17
--建表
drop table if exists all_datatype_tbl;
create table all_datatype_tbl(c_integer integer, c_varchar varchar(50));
--插入数据
insert into all_datatype_tbl values(1,'aaaaa');
--更新c_integer,c_varchar分别为字符型和数值型，报错
update all_datatype_tbl set (c_integer,c_varchar) = (select c_varchar,c_integer from all_datatype_tbl);
--删表
drop table all_datatype_tbl;
