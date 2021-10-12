-- @testpoint: 创建表空间

DROP TABLESPACE IF EXISTS ds_location1;
CREATE TABLESPACE ds_location1 RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';
DROP TABLESPACE IF EXISTS ds_location1;


