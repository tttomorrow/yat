-- @testpoint: hash分区表结合表约束（default） 合理报错

--step1：创建hash分区表 expect：合理报错
drop table if exists partition_hash_tab;
create table partition_hash_tab
(id                        number(7) ,
 use_filename               varchar2(20) ,
 filename                   varchar2(255),
 text                       varchar2(2000),
 default  'aaa'  (filename))
partition by hash(id)
(partition p1,
 partition p2);