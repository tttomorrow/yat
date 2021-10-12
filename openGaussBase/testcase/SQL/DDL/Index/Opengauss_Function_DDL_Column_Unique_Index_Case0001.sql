-- @testpoint: 创建列存表，结合语法参数创建唯一索引

--创建表空间
drop tablespace if exists column_tabspace01;
create tablespace column_tabspace01 relative location 'tablespace/column_space01';

--创建普通列存表
drop table if exists column_tab01;
create table column_tab01(id1 varchar,id2 int) with(orientation=column);

--创建分区列存表
drop table if exists column_part_tab01;
create table column_part_tab01(id float4,name char) with(orientation=column)
partition by range(name)
(partition part_1 values less than('g'),
 partition part_2 values less than('n'),
 partition part_3 values less than('z'));


--普通列存表创建唯一索引（结合语法参数1）
create unique index column_index01_1 on column_tab01 using btree(id1 collate "POSIX")
with(fillfactor=100) tablespace column_tabspace01;

--普通列存表创建唯一索引（结合语法参数2）
create unique index column_index01_2 on column_tab01 using btree(id2 int4_ops);

--分区列存表创建唯一索引（结合语法参数1）
create unique index column_part_index01_1 on column_part_tab01 using btree(name) local;

--分区列存表创建唯一索引（结合语法参数2）
create unique index column_part_index01_2 on column_part_tab01 using btree(name collate "default") local
with(fillfactor=80) tablespace column_tabspace01;

--删除表、表空间
drop table column_tab01 cascade;
drop table column_part_tab01 cascade;
drop tablespace column_tabspace01;
