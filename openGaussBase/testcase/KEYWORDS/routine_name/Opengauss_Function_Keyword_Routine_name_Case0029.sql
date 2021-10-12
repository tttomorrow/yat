--  @testpoint:opengauss关键字routine_name(非保留)，作为表空间名


--关键字不带引号，创建成功
drop tablespace if exists routine_name;
CREATE TABLESPACE routine_name RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';
drop tablespace routine_name;
 
--关键字带双引号，创建成功
drop tablespace if exists "routine_name";
CREATE TABLESPACE "routine_name" RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1'; 
drop tablespace "routine_name";

--关键字带单引号，合理报错
drop tablespace if exists 'routine_name';
CREATE TABLESPACE 'routine_name' RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1'; 

--关键字带反引号，合理报错
drop tablespace if exists `routine_name`;
CREATE TABLESPACE `routine_name` RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';

