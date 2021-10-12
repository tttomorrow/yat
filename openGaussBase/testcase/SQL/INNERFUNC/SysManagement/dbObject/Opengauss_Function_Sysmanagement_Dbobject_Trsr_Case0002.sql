-- @testpoint: pg_total_relation_size(regclass)函数的异常校验，合理报错


create table test (a int)
with(orientation = column)
partition by range (a)
(
        partition test_p1 values less than (88),
        partition test_p2 values less than (99)
);
select pg_total_relation_size('test'::regclass,'test'::regclass,'test'::regclass);
select pg_total_relation_size() from pg_class a where a.relname='test';


select pg_total_relation_size(''::regclass);
select pg_total_relation_size('*&^%$'::regclass) from pg_class a where a.relname='test';

drop table test;