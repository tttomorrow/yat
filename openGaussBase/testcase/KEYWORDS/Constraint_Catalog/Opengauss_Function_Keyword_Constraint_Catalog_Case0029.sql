-- @testpoint: opengauss关键字constraint_catalog(非保留)，作为表空间名，部分测试点合理报错


--关键字不带引号，创建成功
drop tablespace if exists constraint_catalog;
CREATE TABLESPACE constraint_catalog RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';
drop tablespace if exists constraint_catalog;
 
--关键字带双引号，创建成功
drop tablespace if exists "constraint_catalog";
CREATE TABLESPACE "constraint_catalog" RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1'; 
drop tablespace "constraint_catalog";

--关键字带单引号，合理报错
drop tablespace if exists 'constraint_catalog';
CREATE TABLESPACE 'constraint_catalog' RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1'; 

--关键字带反引号，合理报错
drop tablespace if exists `constraint_catalog`;
CREATE TABLESPACE `constraint_catalog` RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';

