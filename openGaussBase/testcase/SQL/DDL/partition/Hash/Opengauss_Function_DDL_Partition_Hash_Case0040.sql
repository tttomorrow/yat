-- @testpoint: Hash分区表结合表约束（not null）合理报错

--step1：创建Hash分区表 expect：合理报错
DROP TABLE IF EXISTS partition_hash_tab;
CREATE TABLE partition_hash_tab
(id                         NUMBER(7),
 use_filename               VARCHAR2(20),
 filename                   VARCHAR2(255),
 text                       VARCHAR2(2000),
 not null(id))
partition by hash(id)
(partition p1,
 partition p2);

--step2：清理环境 expect：成功
--无需清理环境