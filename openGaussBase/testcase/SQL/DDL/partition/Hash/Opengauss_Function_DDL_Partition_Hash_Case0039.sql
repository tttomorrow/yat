-- @testpoint: Hash分区表结合表约束（check） 部分合理报错

--step1：创建Hash分区表 expect：成功
DROP TABLE IF EXISTS partition_hash_tab;
CREATE TABLE partition_hash_tab
(id                int ,
name               VARCHAR2(20) ,
filename           VARCHAR2(255),
text               VARCHAR2(2000),
check(id>0))
partition by hash(id)
(partition p1,
 partition p2);

--step2：插入数据 expect：部分合理报错
insert into  partition_hash_tab values(1,'zhang','text','hahahahah');
insert into  partition_hash_tab values(100,'zhang','text','hahahahah');
insert into  partition_hash_tab values(-1,'zhang','text','hahahahah');

--step3：查询数据 expect：成功
select * from partition_hash_tab;

--step4：清理环境 expect：成功
drop table if exists partition_hash_tab;