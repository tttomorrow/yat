-- @testpoint: 创建普通hash分区表，验证分区个数 合理报错

--step1：分区个数为0 expect：合理报错
drop table if exists partition_hash_tab_num0;
create table partition_hash_tab_num0(p_id int,p_name varchar)
partition by hash(p_id)
();

--step2：分区个数为1 expect：成功
drop table if exists partition_hash_tab_num1;
create table partition_hash_tab_num1(p_id int,p_name varchar)
partition by hash(p_id)
(partition part_1);

--step2：分区个数为2 expect：成功
drop table if exists partition_hash_tab_num2;
create table partition_hash_tab_num2(p_id int,p_name varchar)
partition by hash(p_id)
(partition part_1,
 partition part_2);

--step3：清理环境 expect：成功
drop table if exists partition_hash_tab_num1;
drop table if exists partition_hash_tab_num2;