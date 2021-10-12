-- @testpoint: pg_partition_filenode(partition_oid)函数的异常校验，合理报错

-- 测试多参 少参 空值 特殊字符等
drop table if exists test;
CREATE TABLE test
 (
     sk            INTEGER               NOT NULL,
     id            CHAR(16)              NOT NULL,
     name          VARCHAR(20)                   ,
     grade              DECIMAL(5,2)
 ) WITH (ORIENTATION = COLUMN, COMPRESSION=HIGH);
insert into test values(10,'kk','mmmm','5.21');
select pg_partition_filenode(a.oid::regclass,'test'::regclass) from pg_class a where a.relname='test';
select pg_partition_filenode();
select pg_partition_filenode('') from pg_class a where a.relname='test';
select pg_partition_filenode('*&^%%'::regclass);
drop table test;