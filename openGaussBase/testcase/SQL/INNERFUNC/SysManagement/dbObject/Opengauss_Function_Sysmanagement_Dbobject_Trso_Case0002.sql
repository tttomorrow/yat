-- @testpoint: pg_total_relation_size(oid)函数的异常校验，合理报错


create table test (a int)
with(orientation = column)
partition by range (a)
(
        partition test_p1 values less than (88),
        partition test_p2 values less than (99)
);
select pg_total_relation_size(a.oid,a.oid) from pg_class a where a.relname='test';

create index test_index on test (a) local;
select pg_total_relation_size() from pg_class a where a.relname='test';

insert into test values (59);
insert into test values (90);
select pg_total_relation_size('*&^%&') from pg_class a where a.relname='test';

drop table test;