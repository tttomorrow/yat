-- @testpoint: 创建普通hash分区表，并更改分区表的所属表空间 合理报错

--step1：创建表空间 except：成功
drop tablespace if exists tabspace01;
drop tablespace if exists tabspace02;
create tablespace tabspace01 relative location 'tablespace/tablespace01';
create tablespace tabspace02 relative location 'tablespace/tablespace02';

--step2：创建hash分区表，并指定表空间 except：成功
drop table if exists partition_hash_tab;
create table partition_hash_tab(p_id int,p_age int)
tablespace tabspace01
partition by hash(p_id)
(partition part_1,
 partition part_2);

--step3：插入数据 except：成功
INSERT INTO partition_hash_tab VALUES(1,1);
INSERT INTO partition_hash_tab VALUES(2,2);

--step4：更改分区表所属表空间 except：合理报错
ALTER TABLE partition_hash_tab SET TABLESPACE tabspace02;

--step4：清理环境 except：成功
drop table partition_hash_tab;
drop tablespace tabspace01;
drop tablespace tabspace02;