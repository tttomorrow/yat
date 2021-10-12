-- @testpoint: pg_relation_filenode(relation regclass)接受一个表、索引、序列或压缩表的OID或者名称，并且返回当前分配给它的"filenode"数

-- testpoint:使用名称和oid都能获取到
-- 表
drop table if exists test;
create table test (a int)
with(orientation = column)
partition by range (a)
(
        partition test_p1 values less than (88),
        partition test_p2 values less than (99)
);
select pg_relation_filenode(a.oid::regclass) = pg_relation_filenode('test'::regclass) from pg_class a where a.relname='test';
SELECT strpos(pg_relation_filepath('test'::regclass), text(pg_relation_filenode('test'::regclass))) > 0;
-- 索引
create index test_index on test (a) local;
select pg_relation_filenode(b.oid::regclass) = pg_relation_filenode('test_index'::regclass) from pg_class b where b.relname='test_index';
select pg_relation_filenode('test_index'::regclass)>0;
-- 序列
CREATE SEQUENCE serial1
 START 101
 CACHE 20
OWNED BY test.a;
select pg_relation_filenode(c.oid::regclass) = pg_relation_filenode('serial1'::regclass) from pg_class c where c.relname='serial1';
select pg_relation_filenode('serial1'::regclass) > 0;
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
select pg_relation_filenode(a.oid::regclass) = pg_relation_filenode('test'::regclass) from pg_class a where a.relname='test';
select pg_relation_filenode('test'::regclass)>0;
drop table test;