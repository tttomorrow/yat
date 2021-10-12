-- @testpoint: 删除表空间

--表空间里面没有任何数据库对象
DROP TABLESPACE IF EXISTS re_location1;
CREATE TABLESPACE ds_location1 RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';
DROP TABLESPACE IF EXISTS ds_location1;



--表空间里面有数据库对象

drop table if exists ts_test;
DROP TABLESPACE IF EXISTS re_location1;
CREATE TABLESPACE ds_location1 RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';
CREATE table  ts_test(a int)   tablespace  ds_location1;
DROP TABLE IF EXISTS ts_test;
DROP TABLESPACE IF EXISTS ds_location1;



