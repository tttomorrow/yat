-- @testpoint: 创建一个新的表空间，表空间名字不同，路径不同

DROP TABLESPACE IF EXISTS ds_location1;
CREATE TABLESPACE ds_location1 RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';
DROP TABLESPACE IF EXISTS ds_location5;
CREATE TABLESPACE ds_location5 RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_5';
DROP TABLESPACE IF EXISTS ds_location1;
DROP TABLESPACE IF EXISTS ds_location5;