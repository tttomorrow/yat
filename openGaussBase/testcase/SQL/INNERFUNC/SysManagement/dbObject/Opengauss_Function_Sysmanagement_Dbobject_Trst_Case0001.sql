-- @testpoint:pg_total_relation_size(text)指定名称的表所使用的全部磁盘空间，包括索引和压缩数据。表名称可以用模式名修饰。


-- 分区表
create table test (a int)
with(orientation = column)
partition by range (a)
(
        partition test_p1 values less than (88),
        partition test_p2 values less than (99)
);
select pg_total_relation_size('test');

create index test_index on test (a) local;
select pg_total_relation_size('test');

insert into test values (90);
select pg_total_relation_size('test');

drop table test;

-- 压缩表
CREATE TABLE test
 (
     sk            INTEGER               NOT NULL,
     id            CHAR(16)              NOT NULL,
     name          VARCHAR(20)                   ,
     grade              DECIMAL(5,2)
 ) WITH (ORIENTATION = COLUMN, COMPRESSION=HIGH);
select pg_total_relation_size('test');
insert into test values(10,'kk','mmmm','5.21');
select pg_total_relation_size('test');
drop table test;