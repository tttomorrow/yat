-- @testpoint: 列存表使用update..returning子句，合理报错
--建表
drop table if exists all_datatype_tbl;
create table all_datatype_tbl(c_integer integer, c_varchar varchar(50)) with(orientation = column);
--插入数据
insert into all_datatype_tbl values(1,'aaaaa');
insert into all_datatype_tbl values(2,'bbbbb');
--修改数据，报错
update all_datatype_tbl set c_varchar = 'new_a' where c_integer = 1 returning *;
update all_datatype_tbl set c_varchar = 'new_a' where c_integer = 1 returning c_integer;
--删表
drop table all_datatype_tbl;
