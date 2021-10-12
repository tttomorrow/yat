-- @testpoint: pg_relation_size(oid)指定OID代表的表或者索引所使用的磁盘空间。


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

select pg_relation_size(a.oid) from pg_class a where a.relname='test';
select pg_relation_size(b.oid) from pg_class b where b.relname='test_index';

drop table test;