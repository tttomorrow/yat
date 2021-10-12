-- @testpoint: 子查询中使用join,子查询返回值超过一行，合理报错
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
insert into all_datatype_tbl values(1,'aaaaa');
insert into all_datatype_tbl values(2,'bbbbb');
insert into all_datatype_tbl values(3,'ccccccccc');
insert into all_datatype_tbl values(4,'ddddddddddddd');
insert into all_datatype_tbl values(5,'eeeeeeeeeee');
select * from all_datatype_tbl;
--修改数据
update all_datatype_tbl t1 set (c_integer,c_varchar) = (select t4.c_integer c1,t5.c_varchar c2
from all_datatype_tbl t2, all_datatype_tbl t3, all_datatype_tbl t4, all_datatype_tbl t5
where t1.c_integer=t2.c_integer+1 and t1.c_integer=t3.c_integer);
select * from all_datatype_tbl order by 1;
--删表
drop table if exists all_datatype_tbl;

