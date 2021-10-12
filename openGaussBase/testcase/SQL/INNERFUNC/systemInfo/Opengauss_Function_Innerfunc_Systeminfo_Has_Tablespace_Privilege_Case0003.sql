-- @testpoint: 表空间没有赋予权限时返回为false
DROP USER IF EXISTS joe CASCADE;
drop TABLESPACE if exists tpcds_tbspc;
CREATE TABLESPACE tpcds_tbspc RELATIVE LOCATION 'tablespace/tablespace_1';
CREATE USER joe PASSWORD 'Bigdata@123';
select has_tablespace_privilege ('joe', 'tpcds_tbspc', 'CREATE');
drop TABLESPACE if exists tpcds_tbspc;
DROP USER IF EXISTS joe CASCADE;