-- @testpoint: 表空间参数为oid时权限存在或者不存在时返回值校验
DROP USER IF EXISTS joe CASCADE;
drop TABLESPACE if exists tpcds_tbspc;
CREATE TABLESPACE tpcds_tbspc RELATIVE LOCATION 'tablespace/tablespace_1';
CREATE USER joe PASSWORD 'Bigdata@123';
select has_tablespace_privilege ('joe', oid, 'CREATE') from PG_TABLESPACE where spcname ='tpcds_tbspc';
GRANT ALL PRIVILEGES ON TABLESPACE tpcds_tbspc TO joe;
select has_tablespace_privilege ('joe', oid, 'CREATE') from PG_TABLESPACE where spcname ='tpcds_tbspc';
drop TABLESPACE if exists tpcds_tbspc;
DROP USER IF EXISTS joe CASCADE;