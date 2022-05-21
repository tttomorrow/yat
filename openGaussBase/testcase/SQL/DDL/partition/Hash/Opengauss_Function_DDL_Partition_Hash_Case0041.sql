-- @testpoint: Hash分区表结合列约束（default）默认值和数据类型匹配

--step1：创建hash分区表 expect：成功
drop table if exists partition_hash_tab;
create table partition_hash_tab
(id                int  default '123',
name               varchar2(20),
filename           varchar2(255),
text               varchar2(2000))
partition by hash(id)
(partition p1,
 partition p2);

--step2：插入数据 expect：成功
insert into  partition_hash_tab values(1,'zhang','text','hahahahah');
insert into  partition_hash_tab values(100,'zhang','text','hahahahah');
insert into  partition_hash_tab (name,filename,text )  values('zhang','text','hahahahah');

--step3：查询数据 expect：成功
select * from partition_hash_tab;

--step4：清理环境 expect：成功
drop table if exists partition_hash_tab;