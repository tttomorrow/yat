-- @testpoint: 创建表空间且所有者指定为Joe


DROP TABLESPACE IF EXISTS ds_location4;
DROP role IF EXISTS qwe;
CREATE ROLE qwe IDENTIFIED BY 'Bigdata@123';
CREATE TABLESPACE ds_location4 OWNER qwe RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_2';
DROP TABLESPACE IF EXISTS ds_location4;
DROP role IF EXISTS qwe;