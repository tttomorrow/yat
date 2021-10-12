-- @testpoint: 创建普通hash分区表，验证支持的数据类型（字符类型）

--支持的字符类型char
drop table if exists partition_hash_tab_char;
create table partition_hash_tab_char(p_id int1,p_name char,p_age int)
partition by hash(p_name)
(partition part_1,
 partition part_2);

--支持的字符类型varchar(n)
drop table if exists partition_hash_tab_varchar;
create table partition_hash_tab_varchar(p_id int2,p_name varchar(10),p_age int)
partition by hash(p_name)
(partition part_1,
 partition part_2,
 partition part_3);

--支持的字符类型nvarchar2
drop table if exists partition_hash_tab_nvarchar2;
create table partition_hash_tab_nvarchar2(p_id int4,p_name nvarchar2,p_age int)
partition by hash(p_name)
(partition part_1,
 partition part_2);

--支持的字符类型text
drop table if exists partition_hash_tab_text;
create table partition_hash_tab_text(p_id int8,p_name text,p_age int)
partition by hash(p_name)
(partition part_1,
 partition part_2,
 partition part_3);

--支持的字符类型bpchar
drop table if exists partition_hash_tab_bpchar;
create table partition_hash_tab_bpchar(p_id int8,p_name bpchar,p_age int)
partition by hash(p_name)
(partition part_1,
 partition part_2,
 partition part_3);

--清理环境
drop table if exists partition_hash_tab_char;
drop table if exists partition_hash_tab_varchar;
drop table if exists partition_hash_tab_nvarchar2;
drop table if exists partition_hash_tab_text;
drop table if exists partition_hash_tab_bpchar;
