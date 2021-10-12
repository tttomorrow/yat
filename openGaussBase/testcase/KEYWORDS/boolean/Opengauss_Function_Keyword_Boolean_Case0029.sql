--  @testpoint:opengauss关键字boolean(非保留)，作为表空间名
--关键字不带引号，创建成功
drop tablespace if exists boolean;
CREATE TABLESPACE boolean RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';
--清理环境
drop tablespace boolean;

--关键字带双引号，创建成功
drop tablespace if exists "boolean";
CREATE TABLESPACE "boolean" RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1'; 

--清理环境
drop tablespace "boolean";

--关键字带单引号，合理报错
drop tablespace if exists 'boolean';

--关键字带反引号，合理报错
drop tablespace if exists `boolean`;
