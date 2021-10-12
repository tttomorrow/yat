-- @testpoint: drop index concurrently 不支持列存表分区表 合理报错

-- create COLUMN table
DROP TABLE IF EXISTS ddl_index_case0226;
CREATE TABLE ddl_index_case0226(id INT, first_name text, last_name text) WITH (ORIENTATION = COLUMN);

--create  index
create  index  ddl_index_case0226_idx on ddl_index_case0226(id);

--drop index concurrently fail
drop index concurrently ddl_index_case0226_idx;

-- create partition table
DROP TABLE IF EXISTS ddl_index_case0226_par;
CREATE TABLE ddl_index_case0226_par(
    WR_RETURNED_DATE_SK       INTEGER                       ,
    WR_RETURNED_TIME_SK       INTEGER                       ,
    WR_NET_LOSS               DECIMAL(7,2)
)
PARTITION BY RANGE(WR_RETURNED_DATE_SK)
(
        PARTITION P1 VALUES LESS THAN(2450815),
        PARTITION P2 VALUES LESS THAN(2451179),
        PARTITION P3 VALUES LESS THAN(2451544),
        PARTITION P4 VALUES LESS THAN(2451910),
        PARTITION P5 VALUES LESS THAN(2452275),
        PARTITION P6 VALUES LESS THAN(2452640),
        PARTITION P7 VALUES LESS THAN(2453005),
        PARTITION P8 VALUES LESS THAN(MAXVALUE)
);

--create index
create index ddl_index_case0226_par_idx on ddl_index_case0226_par(WR_RETURNED_DATE_SK);

--drop index success
drop index concurrently ddl_index_case0226_par_idx;

--tearDown drop table
DROP TABLE IF EXISTS ddl_index_case0226;
DROP TABLE IF EXISTS ddl_index_case0226_par;

