--  @testpoint:opengauss关键字public(非保留)，作为表空间名


--关键字不带引号，创建成功
drop tablespace if exists public;
CREATE TABLESPACE public RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';
drop tablespace public;
 
--关键字带双引号，创建成功
drop tablespace if exists "public";
CREATE TABLESPACE "public" RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1'; 
drop tablespace "public";

--关键字带单引号，合理报错
drop tablespace if exists 'public';
 

--关键字带反引号，合理报错
drop tablespace if exists `public`;


