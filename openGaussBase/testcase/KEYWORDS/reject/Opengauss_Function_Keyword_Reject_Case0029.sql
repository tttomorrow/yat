--  @testpoint:openGauss保留关键字reject作为作为表空间名，

--不带引号，合理报错
drop tablespace if exists reject;
CREATE TABLESPACE reject RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';
--加双引号，创建成功
drop tablespace if exists "reject";
CREATE TABLESPACE "reject" RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';

--清理环境
drop tablespace "reject";

--加单引号，合理报错
drop tablespace if exists 'reject';
CREATE TABLESPACE 'reject' RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';

--加反引号，合理报错
drop tablespace if exists `reject`;
CREATE TABLESPACE `reject` RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';