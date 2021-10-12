-- @testpoint: pg_partition_size(text, text)指定名称的分区使用的磁盘空间。其中，第一个text为表名，第二个text为分区名。

create table test (id int8)
with(orientation = column)
partition by range (id)
(
        partition "P1" values less than (1000),
        partition "P2" values less than (2000)
);

INSERT INTO test VALUES(999);
INSERT INTO test VALUES(888);
INSERT INTO test VALUES(1999);

SELECT pg_partition_size('test','P1');
SELECT pg_partition_size('test','P2');

drop table test;