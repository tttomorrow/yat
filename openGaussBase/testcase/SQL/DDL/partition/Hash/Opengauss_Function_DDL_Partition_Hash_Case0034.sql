-- @testpoint: Hash分区表结合if not exists

--step1：创建hash分区表 expect：成功
DROP TABLE IF EXISTS partition_hash_tab;
CREATE TABLE IF not EXISTS partition_hash_tab
(id NUMBER(7) ,
 use_filename               VARCHAR2(20),
 filename                   VARCHAR2(255),
 text                       VARCHAR2(2000))
partition by hash(id)
(partition p1,
 partition p2
);

--step2：插入数据 expect：成功
insert into partition_hash_tab values(1,'李','李四','数学老师'),
(2,'王','王五','物理老师');

--step3：查看数据 expect：成功
select * from partition_hash_tab;

--step4：清理环境 expect：成功
drop table if exists partition_hash_tab;