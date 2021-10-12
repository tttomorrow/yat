-- @testpoint: 结合不同表类型，创建list分区表，不支持的表类型合理报错

--普通行存list分区表
drop table if exists partition_list_tab01;
create table partition_list_tab01(p_id int,p_name varchar,p_age int)
partition by list(p_id)
(partition part_1 values(10),
 partition part_2 values(20),
 partition part_3 values(30));

--普通列存list分区表，不支持合理报错
drop table if exists partition_list_tab02;
create table partition_list_tab02(p_id int,p_name varchar,p_age int)
with (orientation = column)
partition by list(p_id)
(partition part_1 values(10),
 partition part_2 values(20),
 partition part_3 values(30));

--本地临时行存list分区表，不支持合理报错
drop table if exists partition_list_tab03;
create local temporary table partition_list_tab03(p_id int,p_name varchar,p_age int)
partition by list(p_id)
(partition part_1 values(10),
 partition part_2 values(20),
 partition part_3 values(30));

--全局临时行存list分区表，不支持合理报错
drop table if exists partition_list_tab04;
create global temporary table partition_list_tab04(p_id int,p_name varchar,p_age int)
partition by list(p_id)
(partition part_1 values(10),
 partition part_2 values(20),
 partition part_3 values(30));

--清理环境
drop table if exists partition_list_tab01;
drop table if exists partition_list_tab02;
drop table if exists partition_list_tab03;
drop table if exists partition_list_tab04;

