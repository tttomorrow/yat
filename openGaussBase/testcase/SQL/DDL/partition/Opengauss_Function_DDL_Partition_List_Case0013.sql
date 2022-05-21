-- @testpoint: list分区表，支持的功能 row movement
--创建list分区表,指定参数row movement
drop table if exists partition_list_tab;
create table partition_list_tab(p_id int,p_name varchar,p_age int)
partition by list(p_id)
(partition p1 values(10),
 partition p2 values(20),
 partition p3 values(30)) enable row movement;
