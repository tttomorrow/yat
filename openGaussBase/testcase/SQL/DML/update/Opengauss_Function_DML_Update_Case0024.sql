-- @testpoint: 更新列存表数据后，使用vacuum full清理
--建表
drop table if exists all_datatype_tbl;
create table all_datatype_tbl(c_integer integer, c_varchar varchar(50)) with(orientation = column);
--插入数据
insert into all_datatype_tbl values(1,'aaaaa');
insert into all_datatype_tbl values(2,'bbbbb');
--查看表大小
select pg_size_pretty(pg_relation_size('all_datatype_tbl'));
--修改数据
update all_datatype_tbl set c_varchar = 'new_a' where c_integer = 1;
--使用vacuum
vacuum full all_datatype_tbl;
--删表
drop table all_datatype_tbl;