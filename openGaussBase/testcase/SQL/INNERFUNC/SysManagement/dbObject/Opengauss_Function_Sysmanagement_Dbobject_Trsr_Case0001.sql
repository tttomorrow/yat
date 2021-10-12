-- @testpoint:pg_total_relation_size(regclass)指定的表使用的总磁盘空间，包括所有的索引和TOAST数据。


create table test (a int)
with(orientation = column)
partition by range (a)
(
        partition test_p1 values less than (88),
        partition test_p2 values less than (99)
);
select pg_total_relation_size('test'::regclass);
select pg_total_relation_size(a.oid::regclass) from pg_class a where a.relname='test';

create index test_index on test (a) local;
select pg_total_relation_size('test'::regclass);
select pg_total_relation_size(a.oid::regclass) from pg_class a where a.relname='test';

insert into test values (90);
select pg_total_relation_size('test'::regclass);
select pg_total_relation_size(a.oid::regclass) from pg_class a where a.relname='test';

drop table test;