-- @testpoint: pg_relation_filepath(relation regclass)接受一个表、索引、序列或压缩表的OID或者名称，并且返回关系的整个文件路径名
-- 表
drop table if exists test;
create table test (a int)
with(orientation = column)
partition by range (a)
(
        partition test_p1 values less than (88),
        partition test_p2 values less than (99)
);
select pg_relation_filepath(a.oid::regclass) = pg_relation_filepath('test'::regclass) from pg_class a where a.relname='test';
SELECT strpos(pg_relation_filepath('test'::regclass), text(pg_relation_filepath('test'::regclass))) > 0;
-- 索引
create index test_index on test (a) local;
select pg_relation_filepath(b.oid::regclass) = pg_relation_filepath('test_index'::regclass) from pg_class b where b.relname='test_index';
SELECT strpos(pg_relation_filepath('test_index'::regclass), text(pg_relation_filepath('test_index'::regclass))) > 0;

-- 序列
CREATE SEQUENCE serial1
 START 101
 CACHE 20
OWNED BY test.a;
select pg_relation_filepath(c.oid::regclass) = pg_relation_filepath('serial1'::regclass) from pg_class c where c.relname='serial1';
SELECT strpos(pg_relation_filepath('serial1'::regclass), text(pg_relation_filepath('serial1'::regclass))) > 0;

DROP SEQUENCE serial1 cascade;
drop table test;

-- 压缩表
drop table if exists test;
CREATE TABLE test
 (
     sk            INTEGER               NOT NULL,
     id            CHAR(16)              NOT NULL,
     name          VARCHAR(20)                   ,
     grade              DECIMAL(5,2)
 ) WITH (ORIENTATION = COLUMN, COMPRESSION=HIGH);
insert into test values(10,'kk','mmmm','5.21');
select pg_relation_filepath(a.oid::regclass) = pg_relation_filepath('test'::regclass) from pg_class a where a.relname='test';
SELECT strpos(pg_relation_filepath('test'::regclass), text(pg_relation_filepath('test'::regclass))) > 0;
drop table test;