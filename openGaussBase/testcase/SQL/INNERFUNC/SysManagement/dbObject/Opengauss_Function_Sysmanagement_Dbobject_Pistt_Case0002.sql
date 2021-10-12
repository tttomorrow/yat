-- @testpoint: pg_partition_indexes_size(text,text)函数的异常校验，合理报错

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

select pg_partition_indexes_size('test', '');
select pg_partition_indexes_size('testtest', 'test_p2');
select pg_partition_indexes_size('test', 'test_p3');
select pg_partition_indexes_size();
select pg_partition_indexes_size('test', 'test_p2','test', 'test_p1');

drop table test;
