--  @testpoint:opengauss关键字bigint(非保留)，作为表空间名
--关键字不带引号，创建成功
drop tablespace if exists bigint;
CREATE TABLESPACE bigint RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';
--清理环境
drop tablespace bigint;

--关键字带双引号，创建成功
drop tablespace if exists "bigint";
CREATE TABLESPACE "bigint" RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1'; 

--清理环境
drop tablespace "bigint";

--关键字带单引号，合理报错
drop tablespace if exists 'bigint';

--关键字带反引号，合理报错
drop tablespace if exists `bigint`;
