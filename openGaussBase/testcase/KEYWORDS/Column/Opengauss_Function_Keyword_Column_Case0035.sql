-- @testpoint: 定义一个列存表
drop table if exists warehouse_t17;

CREATE TABLE warehouse_t17
(
    W_WAREHOUSE_SK            INTEGER               NOT NULL,
    W_WAREHOUSE_ID            CHAR(16)              NOT NULL,
    W_WAREHOUSE_NAME          VARCHAR(20)                   ,
    W_WAREHOUSE_SQ_FT         INTEGER                       ,
    W_STREET_NUMBER           CHAR(10)
   ) WITH (ORIENTATION = COLUMN, COMPRESSION=HIGH)
  ;
drop table if exists warehouse_t17;