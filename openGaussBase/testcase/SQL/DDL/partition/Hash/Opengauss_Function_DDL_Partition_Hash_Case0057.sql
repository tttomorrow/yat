-- @testpoint: Hash分区表结合LIKE INCLUDING  PARTITION参数 合理报错

--step1：创建hash分区表 expect：成功
drop table if exists partition_hash_tab;
create table partition_hash_tab
(id                         number(7) constraint partition_hash_tab_id_nn not null,
 use_filename               varchar2(20),
 filename                   varchar2(255),
 text                       varchar2(2000))
partition by hash(id)
(partition p1,
 partition p2);

--step2：插入数据 expect：成功
insert into partition_hash_tab values(1,'张三','数学','老师');
insert into partition_hash_tab values(2,'张三','数学','老师');

--step3：结合like including  partition参数建表 expect：合理报错
create table partition_hash_tab_like (like  partition_hash_tab including partition);

--step4：清理环境 expect：成功
drop table if exists partition_hash_tab;
drop table if exists partition_hash_tab_like;