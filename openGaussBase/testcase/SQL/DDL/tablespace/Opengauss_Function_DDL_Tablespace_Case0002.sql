-- @testpoint: 创建表空间，不设置表空间限额


DROP TABLESPACE IF EXISTS ds_location2;
CREATE TABLESPACE ds_location2 RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';
ALTER TABLESPACE ds_location2 RESIZE MAXSIZE 'UNLIMITED';
DROP TABLESPACE IF EXISTS ds_location2;