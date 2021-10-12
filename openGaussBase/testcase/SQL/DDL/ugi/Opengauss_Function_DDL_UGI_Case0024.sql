-- @testpoint: 验证【哈希】分区表【split partition】时，update global index关键字对【btree】类型【普通索引】的重建作用，合理报错

--创建分区表，插入样例数据，建立全局索引
drop table if exists test_ugi_024;
create table test_ugi_024
(
    c_id integer not null,
    c_name varchar(16) default 'omm',
    c_class varchar(20) not null
)
partition by hash(c_id)
(
    partition p1,
    partition p2,
    partition p3,
    partition p4,
    partition p5,
    partition p6
);

insert into test_ugi_024(c_id, c_class) select r, '1-1' from generate_series(1,1000) as r;
insert into test_ugi_024(c_id, c_class) select r, '1-2' from generate_series(1001,2000) as r;
insert into test_ugi_024(c_id, c_class) select r, '1-3' from generate_series(2001,3000) as r;
insert into test_ugi_024(c_id, c_class) select r, '1-4' from generate_series(3001,4000) as r;
insert into test_ugi_024(c_id, c_class) select r, '1-5' from generate_series(4001,5000) as r;
insert into test_ugi_024(c_id, c_class) select r, '1-6' from generate_series(5001,6000) as r;

create index global_index_id_024 on test_ugi_024(c_id) global;
create index global_index_class_024 on test_ugi_024(c_class) global;

--收集统计信息
analyse test_ugi_024;

--确认拆分分区可以破坏全局索引，并使用alter index xxx rebuild重建索引global_index_id_024
--查看分区状态
select t1.relname, partstrategy, boundaries from pg_partition t1, pg_class t2 
where t1.parentid = t2.oid and t2.relname = 'test_ugi_024' and t1.parttype = 'p' order by relname;
--查看执行计划，确认走index scan
explain analyse select * from test_ugi_024 where c_id = 2333;
--拆分分区p2，破坏全局索引
alter table test_ugi_024 split partition p2 at (1500) into (partition p2_1, partition p2_2);

--清理表
drop table test_ugi_024;