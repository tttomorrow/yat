--  @testpoint:openGauss保留关键字symmetric作为作为表空间名

--不带引号，合理报错
drop tablespace if exists symmetric;
CREATE TABLESPACE symmetric RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';

--openGauss保留关键字symmetric作为作为表空间名，加双引号，创建成功
drop tablespace if exists "symmetric";
CREATE TABLESPACE "symmetric" RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';
drop tablespace "symmetric";

--openGauss保留关键字symmetric作为作为表空间名，加单引号，合理报错
drop tablespace if exists 'symmetric';
CREATE TABLESPACE 'symmetric' RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';

--openGauss保留关键字symmetric作为作为表空间名，加反引号，合理报错
drop tablespace if exists `symmetric`;
CREATE TABLESPACE `symmetric` RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';