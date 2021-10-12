--  @testpoint:openGauss保留关键字except作为作为表空间名，不带引号，合理报错
drop tablespace if exists except;
CREATE TABLESPACE except RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';
--openGauss保留关键字except作为作为表空间名，加双引号，创建成功
drop tablespace if exists "except";
CREATE TABLESPACE "except" RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';
drop tablespace "except";
----openGauss保留关键字except作为作为表空间名，加单引号，合理报错
drop tablespace if exists 'except';
CREATE TABLESPACE 'except' RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';
-----openGauss保留关键字except作为作为表空间名，加反引号，合理报错
drop tablespace if exists `except`;
CREATE TABLESPACE `except` RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';