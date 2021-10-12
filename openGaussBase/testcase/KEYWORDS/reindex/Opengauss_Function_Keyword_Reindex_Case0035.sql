--  @testpoint:opengauss关键字reindex(非保留),为表中的数据重建索引


 drop schema if exists tpcds;
 create schema tpcds;
 CREATE TABLE tpcds.customer_t1
(
    c_customer_sk             integer               not null,
    c_customer_id             char(16)              not null
)
WITH (orientation = row);

CREATE INDEX tpcds_customer_index1 ON tpcds.customer_t1 (c_customer_sk);

INSERT INTO  tpcds.customer_t1 values(1,'zhangsan');



--重建一个单独索引。
REINDEX INDEX tpcds.tpcds_customer_index1;

--重建表tpcds.customer_t1上的所有索引。
REINDEX TABLE tpcds.customer_t1;

--删除tpcds.customer_t1表。
DROP TABLE tpcds.customer_t1;

DROP schema tpcds;
