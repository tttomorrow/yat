-- @testpoint: 创建普通list分区表，验证支持的数据类型（字符类型）

--支持的字符类型char
drop table if exists partition_list_tab_char;
create table partition_list_tab_char(p_id int1,p_name char,p_age int)
partition by list(p_name)
(partition part_1 values('A'),
 partition part_2 values('z'));

--支持的字符类型varchar(n)
drop table if exists partition_list_tab_varchar;
create table partition_list_tab_varchar(p_id int2,p_name varchar(10),p_age int)
partition by list(p_name)
(partition part_1 values('abc'),
 partition part_2 values('abcdef'),
 partition part_3 values('abcdefghij'));

--支持的字符类型nvarchar2
drop table if exists partition_list_tab_nvarchar2;
create table partition_list_tab_nvarchar2(p_id int4,p_name nvarchar2,p_age int)
partition by list(p_name)
(partition part_1 values('a'),
 partition part_2 values('ace'));

--支持的字符类型bpchar
drop table if exists partition_list_tab_bpchar;
create table partition_list_tab_bpchar(p_id int8,p_name bpchar,p_age int)
partition by list(p_name)
(partition part_1 values('A'),
 partition part_2 values('H'),
 partition part_3 values('O'));

--清理环境
drop table if exists partition_list_tab_char;
drop table if exists partition_list_tab_varchar;
drop table if exists partition_list_tab_nvarchar2;
drop table if exists partition_list_tab_bpchar;
