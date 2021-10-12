-- @testpoint: 创建一个以‘pg’开头的表空间,合理报错



DROP TABLESPACE IF EXISTS pg_location1;
CREATE TABLESPACE pg_location1 RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_2';

