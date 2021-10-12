-- @testpoint: pg_relation_size(text)指定名称的表或者索引使用的磁盘空间。表名称可以用模式名修饰。

-- 带模式名
create schema tpcds;
CREATE TABLE tpcds.ship_mode_t1
(
    SM_SHIP_MODE_SK           INTEGER               NOT NULL,
    SM_SHIP_MODE_ID           CHAR(16)              NOT NULL,
    SM_TYPE                   CHAR(30)
);
select pg_relation_size('tpcds.ship_mode_t1');
CREATE UNIQUE INDEX ds_ship_mode_t1_index1 ON tpcds.ship_mode_t1(SM_SHIP_MODE_SK);
select pg_relation_size('tpcds.ship_mode_t1');
select pg_relation_size('tpcds.ds_ship_mode_t1_index1');

insert into tpcds.ship_mode_t1 values(3,'hhh','ooo');
select pg_relation_size('tpcds.ship_mode_t1');
select pg_relation_size('tpcds.ds_ship_mode_t1_index1');

DELETE FROM tpcds.ship_mode_t1 WHERE SM_SHIP_MODE_SK = 3;
select pg_relation_size('tpcds.ship_mode_t1');
select pg_relation_size('tpcds.ds_ship_mode_t1_index1');

DROP INDEX tpcds.ds_ship_mode_t1_index1;
VACUUM FULL tpcds.ship_mode_t1;
select pg_relation_size('tpcds.ship_mode_t1');
DROP TABLE tpcds.ship_mode_t1;
DROP schema tpcds;

-- 不带模式名
CREATE TABLE customer_t1
(
    c_customer_sk             integer,
    c_customer_id             char(5)
);
select pg_relation_size('customer_t1');
CREATE UNIQUE INDEX index1 ON customer_t1(c_customer_sk);
select pg_relation_size('customer_t1');
select pg_relation_size('index1');

insert into customer_t1 values(9,'hhh');
insert into customer_t1 values(8,'ooo');
select pg_relation_size('customer_t1');
select pg_relation_size('index1');

DELETE FROM customer_t1 WHERE c_customer_sk < 10;
select pg_relation_size('customer_t1');
select pg_relation_size('index1');

DROP INDEX index1;
VACUUM FULL customer_t1;
select pg_relation_size('customer_t1');
DROP TABLE customer_t1;