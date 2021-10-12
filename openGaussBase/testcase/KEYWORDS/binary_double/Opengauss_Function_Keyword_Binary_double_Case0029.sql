--  @testpoint:opengauss关键字binary_double(非保留)，作为表空间名
--关键字不带引号，创建成功
drop tablespace if exists binary_double;
CREATE TABLESPACE binary_double RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';
--清理环境
drop tablespace binary_double;

--关键字带双引号，创建成功
drop tablespace if exists "binary_double";
CREATE TABLESPACE "binary_double" RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1'; 

--清理环境
drop tablespace "binary_double";

--关键字带单引号，合理报错
drop tablespace if exists 'binary_double';

--关键字带反引号，合理报错
drop tablespace if exists `binary_double`;
