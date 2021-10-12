-- @testpoint: 创建列存表

DROP TABLE IF EXISTS warehouse_t10;
CREATE TABLE warehouse_t10
(
    W_WAREHOUSE_SK            INTEGER               NOT NULL,
    W_WAREHOUSE_id         CHAR(16)              NOT NULL,
    W_WAREHOUSE_name         VARCHAR(20)                   ,
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
) WITH (ORIENTATION = COLUMN);
DROP TABLE IF EXISTS warehouse_t10;


