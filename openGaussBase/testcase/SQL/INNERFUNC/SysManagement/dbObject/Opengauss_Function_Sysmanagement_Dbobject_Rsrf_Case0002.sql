-- @testpoint: pg_relation_size(relation regclass, fork text)函数的异常校验，合理报错


CREATE TABLE test
(
    c_customer_sk             integer,
    c_customer_id             char(5)
);
CREATE UNIQUE INDEX test_index ON test(c_customer_sk);
insert into test values(9,'hhh');
insert into test values(8,'ooo');

select pg_relation_size(a.oid,'main','main') from pg_class a where a.relname='test';
select pg_relation_size() from pg_class a where a.relname='test';

select pg_relation_size(b.oid,'*&^%$') from pg_class b where b.relname='test_index';
select pg_relation_size('','') from pg_class b where b.relname='test_index';
select pg_relation_size('') from pg_class a where a.relname='test';
drop table test;