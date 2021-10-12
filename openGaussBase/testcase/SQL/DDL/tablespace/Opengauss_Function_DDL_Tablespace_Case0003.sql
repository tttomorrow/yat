-- @testpoint: 创建表空间，设置表空间限额
DROP TABLESPACE IF EXISTS ds_location3;
CREATE TABLESPACE ds_location3 RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';
DROP TABLESPACE IF EXISTS ds_location3;