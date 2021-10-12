-- @testpoint: 重命名表空间



DROP TABLESPACE IF EXISTS ds_location1;
CREATE TABLESPACE ds_location1 RELATIVE LOCATION 'hdfs_tablespace/hdfs_tablespace_1';
ALTER TABLESPACE ds_location1 RENAME TO re_location1;
DROP TABLESPACE IF EXISTS ds_location1;
DROP TABLESPACE IF EXISTS re_location1;