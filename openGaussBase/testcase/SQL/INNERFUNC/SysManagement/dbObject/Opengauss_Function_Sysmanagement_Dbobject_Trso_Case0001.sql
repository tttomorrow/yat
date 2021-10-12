-- @testpoint: pg_total_relation_size(oid)指定OID代表的表使用的磁盘空间，包括索引和压缩数据。


-- 分区表
create table test (a int)
with(orientation = column)
partition by range (a)
(
        partition test_p1 values less than (88),
        partition test_p2 values less than (99)
);
select pg_total_relation_size(a.oid) from pg_class a where a.relname='test';

create index test_index on test (a) local;
select pg_total_relation_size(a.oid) from pg_class a where a.relname='test';

insert into test values (59);
insert into test values (90);
select pg_total_relation_size(a.oid) from pg_class a where a.relname='test';

drop table test;

-- 压缩表
CREATE TABLE test
 (
     sk            INTEGER               NOT NULL,
     id            CHAR(16)              NOT NULL,
     name          VARCHAR(20)                   ,
     grade              DECIMAL(5,2)
 ) WITH (ORIENTATION = COLUMN, COMPRESSION=HIGH);
insert into test values(10,'kk','mmmm','5.21');
select pg_total_relation_size(a.oid) from pg_class a where a.relname='test';
drop table test;