-- @testpoint: 修改列存表唯一索引，修改索引空间

--创建表空间
drop tablespace if exists column_tabspace03_1;
drop tablespace if exists column_tabspace03_2;
create tablespace column_tabspace03_1 relative location 'tablespace/column_space031';
create tablespace column_tabspace03_2 relative location 'tablespace/column_space032';

--创建普通列存表
drop table if exists column_tab03;
create table column_tab03(id1 varchar,id2 int) with(orientation=column);

--创建分区列存表
drop table if exists column_part_tab03;
create table column_part_tab03(id int,name varchar) with(orientation=column)
partition by range(id)
(partition part_1 values less than(1000),
 partition part_2 values less than(2000),
 partition part_3 values less than(maxvalue));

--创建普通列存表唯一索引,指定表空间
create unique index column_index03 on column_tab03 using cbtree(id1) tablespace column_tabspace03_1;

--创建列存分区表唯一索引,指定表空间
create unique index column_part_index03 on column_part_tab03 using cbtree(id) local tablespace column_tabspace03_1;

--修改索引表空间
alter index column_index03 set tablespace column_tabspace03_2;
alter index column_part_index03 move partition part_2_id_idx tablespace column_tabspace03_2;

--清理环境
drop table column_tab03 cascade;
drop table column_part_tab03 cascade;
drop tablespace column_tabspace03_1;
drop tablespace column_tabspace03_2;
