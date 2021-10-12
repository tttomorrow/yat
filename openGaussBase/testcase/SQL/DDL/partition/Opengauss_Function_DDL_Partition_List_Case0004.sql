-- @testpoint: 创建普通list分区表，验证支持的数据类型（数值类型）

--支持的数值类型int1
drop table if exists partition_list_tab_int1;
create table partition_list_tab_int1(p_id int1,p_name varchar,p_age int)
partition by list(p_id)
(partition part_1 values(255));

--支持的数值类型int2
drop table if exists partition_list_tab_int2;
create table partition_list_tab_int2(p_id int2,p_name varchar,p_age int)
partition by list(p_id)
(partition part_1 values(32767));

--支持的数值类型int4
drop table if exists partition_list_tab_int4;
create table partition_list_tab_int4(p_id int4,p_name varchar,p_age int)
partition by list(p_id)

--支持的数值类型int8
drop table if exists partition_list_tab_int8;
create table partition_list_tab_int8(p_id int8,p_name varchar,p_age int)
partition by list(p_id)

--支持的数值类型numeric
drop table if exists partition_list_tab_numeric;
create table partition_list_tab_numeric(p_id numeric(10,3),p_name varchar,p_age int)
partition by list(p_id)
(partition part_1 values(0.123));

--清理环境
drop table if exists partition_list_tab_int1;
drop table if exists partition_list_tab_int2;
drop table if exists partition_list_tab_int4;
drop table if exists partition_list_tab_int8;
drop table if exists partition_list_tab_numeric;

