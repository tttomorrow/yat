-- @testpoint: pg_partition_indexes_size(oid,oid)函数的异常校验，合理报错


create table test (a int)
with(orientation = column)
partition by range (a)
(
        partition test_p1 values less than (88),
        partition test_p2 values less than (99)
);
create index test_index on test (a) local;

insert into test values (59);
insert into test values (69);
insert into test values (90);

select pg_partition_indexes_size() from pg_class a, pg_partition b where a.oid=b.parentid and a.relname='test' and b.relname='test_p1';

select pg_partition_indexes_size(a.oid, '') from pg_class a, pg_partition b where a.oid=b.parentid and a.relname='test' and b.relname='test_p2';
select pg_partition_indexes_size('', b.oid) from pg_class a, pg_partition b where a.oid=b.parentid and a.relname='test' and b.relname='test_p1';

select pg_partition_indexes_size(a.oid, b.oid, b.oid) from pg_class a, pg_partition b where a.oid=b.parentid and a.relname='test' and b.relname='test_p2';
select pg_partition_indexes_size(a.oid, 'hijk') from pg_class a, pg_partition b where a.oid=b.parentid and a.relname='test' and b.relname='test_p2';
select pg_partition_indexes_size('hijk', b.oid) from pg_class a, pg_partition b where a.oid=b.parentid and a.relname='test' and b.relname='test_p2';

drop table test;
