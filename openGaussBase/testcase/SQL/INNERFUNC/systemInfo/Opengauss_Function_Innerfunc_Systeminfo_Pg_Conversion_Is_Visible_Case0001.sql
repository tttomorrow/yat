-- @testpoint: 该转换是否在搜索路径中可见
drop SCHEMA if exists my_tpcds;
CREATE SCHEMA my_tpcds;
SET SEARCH_PATH TO my_tpcds, public;
show search_path;
select pg_conversion_is_visible(oid) from PG_CONVERSION where conname ='ascii_to_mic';
drop SCHEMA if exists my_tpcds;
