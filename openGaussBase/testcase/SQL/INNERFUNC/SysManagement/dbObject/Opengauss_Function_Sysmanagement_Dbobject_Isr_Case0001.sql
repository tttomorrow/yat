-- @testpoint: pg_indexes_size(regclass)附加到指定表的索引使用的总磁盘空间。
alter system set autovacuum to off;
drop schema if exists tpcds;
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
select pg_indexes_size('tpcds.ship_mode_t1'::regclass);
CREATE UNIQUE INDEX ds_ship_mode_t1_index1 ON tpcds.ship_mode_t1(SM_SHIP_MODE_SK);
select pg_indexes_size('tpcds.ship_mode_t1'::regclass);

CREATE INDEX ds_ship_mode_t1_index4 ON tpcds.ship_mode_t1 USING btree(SM_SHIP_MODE_SK);
CREATE INDEX ds_ship_mode_t1_index2 ON tpcds.ship_mode_t1(SUBSTR(SM_CODE,1 ,4));
CREATE UNIQUE INDEX ds_ship_mode_t1_index3 ON tpcds.ship_mode_t1(SM_SHIP_MODE_SK) WHERE SM_SHIP_MODE_SK>10;
select pg_indexes_size('tpcds.ship_mode_t1'::regclass);

ALTER INDEX tpcds.ds_ship_mode_t1_index1 RENAME TO ds_ship_mode_t1_index5;
ALTER INDEX tpcds.ds_ship_mode_t1_index2 UNUSABLE;
select pg_indexes_size('tpcds.ship_mode_t1'::regclass);

ALTER INDEX tpcds.ds_ship_mode_t1_index2 REBUILD;
select pg_indexes_size('tpcds.ship_mode_t1'::regclass);

insert into tpcds.ship_mode_t1 values(10,'a','b','c','d','e');
select pg_indexes_size('tpcds.ship_mode_t1'::regclass);

delete from tpcds.ship_mode_t1 where SM_SHIP_MODE_SK = 10;
select pg_indexes_size('tpcds.ship_mode_t1'::regclass);

drop index tpcds.ds_ship_mode_t1_index2;
select pg_indexes_size('tpcds.ship_mode_t1'::regclass);

drop table tpcds.ship_mode_t1;
drop schema tpcds;


