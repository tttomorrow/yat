-- @testpoint: 搜索路径中的模式名称
DROP SCHEMA IF EXISTS tpcds;
CREATE SCHEMA tpcds;
SET SEARCH_PATH TO tpcds, public;
SELECT current_schemas(true);
SELECT current_schemas(false);
DROP SCHEMA IF EXISTS tpcds;