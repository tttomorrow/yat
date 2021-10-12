-- @testpoint: 创建一个已经存在的表空间，表空间名字相同，路径不同,合理报错

DROP TABLESPACE IF EXISTS ds_location1;
CREATE TABLESPACE ds_location1 RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';
CREATE TABLESPACE ds_location1 RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_3';
DROP TABLESPACE IF EXISTS ds_location1;

