-- @testpoint: 更新字段名，字段名更新两次，合理报错
-- @modify at: 2020-11-17
--建表
drop table if exists all_datatype_tbl;
create table all_datatype_tbl(c_integer integer, c_varchar varchar(50));
--插入数据
insert into all_datatype_tbl values(1,'aaaaa');
insert into all_datatype_tbl values(2,'bbbbb');
insert into all_datatype_tbl values(3,'ccccccccc');
insert into all_datatype_tbl values(4,'ddddddddddddd');
insert into all_datatype_tbl values(5,'eeeeeeeeeee');
--合理报错
update all_datatype_tbl t1 set (t1.c_integer,t1.c_integer) = (select c_integer  c1,c_integer c2 from all_datatype_tbl);
--删表
drop table all_datatype_tbl;
