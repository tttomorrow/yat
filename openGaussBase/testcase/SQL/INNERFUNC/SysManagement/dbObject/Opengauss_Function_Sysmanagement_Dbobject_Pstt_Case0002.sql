-- @testpoint: pg_partition_size(text, text)函数的异常校验，合理报错

create table test (id int8)
with(orientation = column)
partition by range (id)
(
        partition "P1" values less than (1000),
        partition "P2" values less than (2000)
);

INSERT INTO test VALUES(999);
INSERT INTO test VALUES(888);

SELECT pg_partition_size('testtest','P1');
SELECT pg_partition_size('test','P3');
SELECT pg_partition_size('test','P1','P2');
SELECT pg_partition_size('test');
SELECT pg_partition_size();

SELECT pg_partition_size('','P3');
SELECT pg_partition_size('test','');
drop table test;