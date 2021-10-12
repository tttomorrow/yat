-- @testpoint: 表空间赋予create权限时返回为true
DROP USER IF EXISTS joe CASCADE;
drop TABLESPACE if exists tpcds_tbspc;
CREATE TABLESPACE tpcds_tbspc RELATIVE LOCATION 'tablespace/tablespace_1';
CREATE USER joe PASSWORD 'Bigdata@123';
GRANT CREATE  ON TABLESPACE tpcds_tbspc TO joe;
select has_tablespace_privilege ('joe', 'tpcds_tbspc', 'CREATE');
drop TABLESPACE if exists tpcds_tbspc;
DROP USER IF EXISTS joe CASCADE;