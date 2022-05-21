-- @testpoint: Hash分区表结合LIKE INCLUDING  INDEXES参数 合理报错

--step1：创建hash分区表 expect：成功
drop table if exists partition_hash_tab;
drop table if exists partition_hash_tab_like;
create table partition_hash_tab
(id                        number(7) constraint pk_tab primary key using index,
 use_filename               varchar2(20) ,
 filename                   varchar2(255),
 text                       varchar2(2000))
partition by hash(id)
(partition p1,
 partition p2);

--step2：插入数据 expect：成功
insert into partition_hash_tab values(1,'李','李四','数学老师');

--step3：结合like参数建表 expect：合理报错
create table partition_hash_tab_like (like  partition_hash_tab including indexes);

--step4：清理环境 expect：成功
drop table if exists partition_hash_tab;
drop table if exists partition_hash_tab_like;