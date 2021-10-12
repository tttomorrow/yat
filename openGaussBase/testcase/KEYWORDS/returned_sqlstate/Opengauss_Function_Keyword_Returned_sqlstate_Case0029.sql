--  @testpoint:opengauss关键字returned_sqlstate(非保留)，作为表空间名
--关键字不带引号，创建成功
drop tablespace if exists returned_sqlstate;
CREATE TABLESPACE returned_sqlstate RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';
--清理环境
drop tablespace returned_sqlstate;

--关键字带双引号，创建成功
drop tablespace if exists "returned_sqlstate";
CREATE TABLESPACE "returned_sqlstate" RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1'; 

--清理环境
drop tablespace "returned_sqlstate";

--关键字带单引号，合理报错
drop tablespace if exists 'returned_sqlstate';

--关键字带反引号，合理报错
drop tablespace if exists `returned_sqlstate`;
