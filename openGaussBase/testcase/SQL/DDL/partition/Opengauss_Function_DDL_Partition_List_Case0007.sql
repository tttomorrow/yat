-- @testpoint: 创建普通list分区表，验证不支持的数据类型，合理报错

--不支持的数据类型：float
drop table if exists partition_list_tab_t1;
create table partition_list_tab_t1(p_id float,p_name char)
partition by list(p_id)
(partition part_1 values(0.1),
 partition part_2 values(0.5));

--不支持的数据类型：bool
drop table if exists partition_list_tab_t2;
create table partition_list_tab_t2(p_id int,p_name char,p_status bool)
partition by list(p_status)
(partition part_1 values(true),
 partition part_2 values(false));

--不支持的数据类型：二进制类型
drop table if exists partition_list_tab_t3;
create table partition_list_tab_t3(p_id raw,p_name char,p_date date)
partition by list(p_id)
(partition part_1 values(hextoraw('AAAABBBB')),
 partition part_2 values(hextoraw('CCCCDDDD')),
 partition part_3 values(hextoraw('EEEEFFFF')),
 partition part_4 values(hextoraw('ABCDEFEF')),
 partition part_5 values(hextoraw('CDCDCDCD')));

--不支持的数据类型，几何类型
drop table if exists partition_list_tab_t4;
create table partition_list_tab_t2(p_id int,p_name char,p_dir point)
partition by list(p_dir)
(partition part_1 values('0,0'),
 partition part_2 values('1,1'));

--清理环境
--No need to clean