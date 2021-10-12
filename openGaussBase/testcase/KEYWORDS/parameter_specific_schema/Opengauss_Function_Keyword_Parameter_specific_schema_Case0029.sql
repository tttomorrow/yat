--  @testpoint:opengauss关键字parameter_specific_schema(非保留)，作为表空间名


--关键字不带引号，创建成功
drop tablespace if exists parameter_specific_schema;
CREATE TABLESPACE parameter_specific_schema RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';
drop tablespace parameter_specific_schema;
 
--关键字带双引号，创建成功
drop tablespace if exists "parameter_specific_schema";
CREATE TABLESPACE "parameter_specific_schema" RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1'; 
drop tablespace "parameter_specific_schema";

--关键字带单引号，合理报错
drop tablespace if exists 'parameter_specific_schema';
CREATE TABLESPACE 'parameter_specific_schema' RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1'; 

--关键字带反引号，合理报错
drop tablespace if exists `parameter_specific_schema`;
CREATE TABLESPACE `parameter_specific_schema` RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';

