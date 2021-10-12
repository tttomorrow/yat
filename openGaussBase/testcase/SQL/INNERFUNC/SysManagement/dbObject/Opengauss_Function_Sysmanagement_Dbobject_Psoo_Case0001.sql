-- @testpoint: pg_partition_size(oid,oid)指定OID代表的分区使用的磁盘空间。其中，第一个oid为表的OID，第二个oid为分区的OID。

CREATE TABLESPACE example1 RELATIVE LOCATION 'tablespace1/tablespace_1';
CREATE TABLESPACE example2 RELATIVE LOCATION 'tablespace2/tablespace_2';
CREATE TABLE test
(
    ca_address_sk       integer                  NOT NULL   ,
    ca_location_type    character(20)
)
TABLESPACE example1
PARTITION BY RANGE (ca_address_sk)
(
        PARTITION "P1" VALUES LESS THAN(5000),
        PARTITION "P2" VALUES LESS THAN(10000),
        PARTITION "P3" VALUES LESS THAN(15000),
        PARTITION "P4" VALUES LESS THAN(20000),
        PARTITION "P5" VALUES LESS THAN(MAXVALUE) TABLESPACE example2
)
ENABLE ROW MOVEMENT;

insert into test values(4000,'urban');
insert into test values(15001,'urban');
insert into test values(15003,'urban');
insert into test values(15999,'city');
insert into test values(10000,'city');

select pg_partition_size(a.oid, b.oid) from pg_class a, pg_partition b where a.oid=b.parentid and a.relname='test' and b.relname='P1';
select pg_partition_size(a.oid, b.oid) from pg_class a, pg_partition b where a.oid=b.parentid and a.relname='test' and b.relname='P2';
select pg_partition_size(a.oid, b.oid) from pg_class a, pg_partition b where a.oid=b.parentid and a.relname='test' and b.relname='P3';
select pg_partition_size(a.oid, b.oid) from pg_class a, pg_partition b where a.oid=b.parentid and a.relname='test' and b.relname='P4';
select pg_partition_size(a.oid, b.oid) from pg_class a, pg_partition b where a.oid=b.parentid and a.relname='test' and b.relname='P5';

DROP TABLE test;
DROP TABLESPACE example1;
DROP TABLESPACE example2;
