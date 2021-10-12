-- @testpoint: opengauss关键字cursor(非保留)，作为表空间名，部分测试点合理报错


--关键字不带引号，创建成功
drop tablespace if exists cursor;
CREATE TABLESPACE cursor RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';
drop tablespace if exists cursor;

--关键字带双引号，创建成功
drop tablespace if exists "cursor";
CREATE TABLESPACE "cursor" RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1'; 
drop tablespace "cursor";

--关键字带单引号，合理报错
drop tablespace if exists 'cursor';
CREATE TABLESPACE 'cursor' RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1'; 

--关键字带反引号，合理报错
drop tablespace if exists `cursor`;
CREATE TABLESPACE `cursor` RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';

