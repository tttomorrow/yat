-- @testpoint: 设置表的所属模式

drop schema if exists myschema1 cascade;
DROP TABLE IF EXISTS warehouse_t1;
CREATE TABLE warehouse_t1
(
    W_WAREHOUSE_SK            INTEGER               PRIMARY KEY CHECK (W_WAREHOUSE_SK > 0),
    W_WAREHOUSE_id         CHAR(16)              NOT NULL,
    W_WAREHOUSE_name         VARCHAR(20)           CHECK (W_WAREHOUSE_NAME IS NOT NULL),
    W_WAREHOUSE_SQ_FT         INTEGER                       ,
    W_STREET_NUMBER           CHAR(10)                      ,
    W_STREET_name            VARCHAR(60)                   ,
    W_STREET_TYPE             CHAR(15)                      ,
    W_SUITE_NUMBER            CHAR(10)                      ,
    W_CITY                    VARCHAR(60)                   ,
    W_COUNTY                  VARCHAR(30)                   ,
    W_STATE                   CHAR(2)                       ,
    W_ZIP                     CHAR(10)                      ,
    W_COUNTRY                 VARCHAR(20)                   ,
    W_GMT_OFFSET             decimal(5,2)
);
CREATE SCHEMA myschema1;
ALTER TABLE IF EXISTS warehouse_t1
    SET SCHEMA myschema1;
DROP TABLE IF EXISTS warehouse_t1;
drop schema myschema1 cascade;