-- @testpoint: Hash分区表结合列约束（PRIMARY KEY） 重复插入相同的值，第二次合理报错

--step1：创建hash分区表 expect：成功
drop table if exists partition_hash_tab;
create table if not exists partition_hash_tab
(id                         number(7)primary key,
 use_filename               varchar2(20),
 filename                   varchar2(255),
 text                       varchar2(2000))
partition by hash(id)
(partition p1,
 partition p2);

--step2：插入数据 expect：成功
insert into partition_hash_tab values(1,'李','李四','数学老师');

--step3：插入数据 expect：primary key约束导致合理报错
insert into partition_hash_tab values(1,'王','王五','化学老师');

--step4：查询数据 expect：只包含step1插入的数值
select * from  partition_hash_tab;

--step5：清理环境 expect：成功
drop table if exists partition_hash_tab;