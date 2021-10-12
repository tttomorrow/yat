-- @testpoint: pg_partition_indexes_size(text,text)指定名称的分区的索引使用的磁盘空间。其中，第一个text为表名，第二个text为分区名。

create table test (a int)
with(orientation = column)
partition by range (a)
(
        partition test_p1 values less than (88),
        partition test_p2 values less than (99)
);
create index test_index on test (a) local;

insert into test values (59);
insert into test values (69);
insert into test values (90);

select pg_partition_indexes_size('test', 'test_p1');
select pg_partition_indexes_size('test', 'test_p2');

drop table test;