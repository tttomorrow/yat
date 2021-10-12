-- @testpoint: 修改列存表唯一索引，修改索引存储参数

--创建普通列存表
drop table if exists column_tab04;
create table column_tab04(id1 varchar,id2 int) with(orientation=column);

--创建分区列存表
drop table if exists column_part_tab04;
create table column_part_tab04(id int,name varchar) with(orientation=column)
partition by range(id)
(partition part_1 values less than(1000),
 partition part_2 values less than(2000),
 partition part_3 values less than(maxvalue));

--创建普通列存表唯一索引
create unique index column_index04 on column_tab04 using cbtree(id1);

--创建列存分区表唯一索引
create unique index column_part_index04 on column_part_tab04 using cbtree(id) local;

--修改索引存储参数
alter index column_index04 set (fillfactor=20);
alter index column_part_index04 set (fillfactor=60);


--清理环境
drop table column_tab04 cascade;
drop table column_part_tab04 cascade;
