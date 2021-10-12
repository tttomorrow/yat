-- @testpoint: 创建普通list分区表，验证分区键值数量，超过64个 合理报错

--分区键值数量为0，合理报错
drop table if exists partition_list_tab01;
create table partition_list_tab01(p_id int,p_name varchar,p_age int)
partition by list(p_id)
(partition part_1 values());

 --分区键值数量小于64
drop table if exists partition_list_tab02;
create table partition_list_tab02(p_id int,p_name varchar,p_age int)
partition by list(p_id)
(partition part_1 values(10,20,30),
 partition part_2 values(40,50,60,70,80,90,100),
 partition part_3 values(200,300,400,500,600,700,800,900,1000,2000));

--分区键值数量为64
drop table if exists partition_list_tab03;
create table partition_list_tab03(p_id int,p_name varchar,p_age int)
partition by list(p_id)
(partition part_1 values(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,
 21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,
 46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64));

--分区键值数量为65,合理报错
drop table if exists partition_list_tab04;
create table partition_list_tab04(p_id int,p_name varchar,p_age int)
partition by list(p_id)
(partition part_1 values(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,
 21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,
 46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65));

--清理环境
drop table if exists partition_list_tab01;
drop table if exists partition_list_tab02;
drop table if exists partition_list_tab03;
drop table if exists partition_list_tab04;

