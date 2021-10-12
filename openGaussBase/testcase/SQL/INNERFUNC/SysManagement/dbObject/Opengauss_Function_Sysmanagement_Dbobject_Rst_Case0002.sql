-- @testpoint: pg_relation_size(text)函数的异常校验，合理报错

create schema tpcds;
CREATE TABLE tpcds.ship_mode_t1
(
    SM_SHIP_MODE_SK           INTEGER               NOT NULL,
    SM_SHIP_MODE_ID           CHAR(16)              NOT NULL,
    SM_TYPE                   CHAR(30)
);
CREATE UNIQUE INDEX ds_ship_mode_t1_index1 ON tpcds.ship_mode_t1(SM_SHIP_MODE_SK);
select pg_relation_size('ship_mode_t1');
select pg_relation_size('ds_ship_mode_t1_index1');
select pg_relation_size('tpcdsds_ship_mode_t1_index1');
select pg_relation_size('tpcds-ds_ship_mode_t1_index1');
select pg_relation_size('nofile');

select pg_relation_size('');
select pg_relation_size();
select pg_relation_size('tpcds.ship_mode_t1','tpcds.ds_ship_mode_t1_index1','tpcds.ship_mode_t1');

DROP INDEX tpcds.ds_ship_mode_t1_index1;
DROP TABLE tpcds.ship_mode_t1;
DROP schema tpcds;
