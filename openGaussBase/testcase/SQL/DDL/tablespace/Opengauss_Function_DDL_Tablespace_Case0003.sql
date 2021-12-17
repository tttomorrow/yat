-- @testpoint: 创建表空间，设置表空间限额
DROP TABLESPACE IF EXISTS ds_location3;
CREATE TABLESPACE ds_location3 RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';
ALTER TABLESPACE ds_location3  RESIZE MAXSIZE  '9007199254740991K';
DROP TABLESPACE IF EXISTS ds_location3;