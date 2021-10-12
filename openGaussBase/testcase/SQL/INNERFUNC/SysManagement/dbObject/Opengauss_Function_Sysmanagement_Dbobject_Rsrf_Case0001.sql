-- @testpoint: pg_relation_size(relation regclass, fork text)指定表或索引的指定分叉树（'main'，'fsm'或'vm'）使用的磁盘空间。


CREATE TABLE test
(
    c_customer_sk             integer,
    c_customer_id             char(5)
);
CREATE UNIQUE INDEX test_index ON test(c_customer_sk);
insert into test values(9,'hhh');
insert into test values(8,'ooo');

select pg_relation_size(a.oid,'main') from pg_class a where a.relname='test';
select pg_relation_size(a.oid,'fsm') from pg_class a where a.relname='test';
select pg_relation_size(a.oid,'vm') from pg_class a where a.relname='test';
select pg_relation_size(b.oid,'main') from pg_class b where b.relname='test_index';
select pg_relation_size(b.oid,'fsm') from pg_class b where b.relname='test_index';
select pg_relation_size(b.oid,'vm') from pg_class b where b.relname='test_index';

drop table test;