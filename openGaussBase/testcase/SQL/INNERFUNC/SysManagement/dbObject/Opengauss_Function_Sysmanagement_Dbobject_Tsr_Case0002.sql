-- @testpoint: pg_table_size(regclass)函数的异常校验，合理报错

create schema tpcds;
CREATE TABLE tpcds.ship_mode_t1
(
    SM_SHIP_MODE_SK           INTEGER               NOT NULL,
    SM_SHIP_MODE_ID           CHAR(16)              NOT NULL,
    SM_TYPE                   CHAR(30)                      ,
    SM_CODE                   CHAR(10)                      ,
    SM_CARRIER                CHAR(20)                      ,
    SM_CONTRACT               CHAR(20)
);

select pg_table_size('tpcds.ship_mode_t1'::regclass);

CREATE UNIQUE INDEX ds_ship_mode_t1_index1 ON tpcds.ship_mode_t1(SM_SHIP_MODE_SK);
select pg_table_size(regclass 'ship_mode_t1');
select pg_table_size('tpcds.ship_mode_t1','tpcds.ship_mode_t1'::regclass);

select pg_table_size();
select pg_table_size('');

drop table tpcds.ship_mode_t1;
drop schema tpcds;
