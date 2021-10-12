-- @testpoint: 验证【哈希】分区表【exchange partition】时，update global index关键字对【btree】类型【唯一性多字段索引】的重建作用，合理报错

--创建分区表，插入样例数据，建立全局索引
drop table if exists test_ugi_037;
create table test_ugi_037
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

insert into test_ugi_037(c_id, c_class) select r, '1-1' from generate_series(1,1000) as r;
insert into test_ugi_037(c_id, c_class) select r, '1-2' from generate_series(1001,2000) as r;
insert into test_ugi_037(c_id, c_class) select r, '1-3' from generate_series(2001,3000) as r;
insert into test_ugi_037(c_id, c_class) select r, '1-4' from generate_series(3001,4000) as r;
insert into test_ugi_037(c_id, c_class) select r, '1-5' from generate_series(4001,5000) as r;
insert into test_ugi_037(c_id, c_class) select r, '1-6' from generate_series(5001,6000) as r;

create unique index global_index_id_037 on test_ugi_037(c_id,  c_name) global;

--创建exchange用的普通表
drop table if exists test_ugi_037_temp;
create table test_ugi_037_temp
(
    c_id integer not null,
    c_name varchar(16) default 'omm',
    c_class varchar(20) not null
);
insert into test_ugi_037_temp(c_id, c_class) select r, '1-4' from generate_series(3001,3500) as r;

--收集统计信息
analyse test_ugi_037;

--确认交换分区可以破坏全局索引，并使用alter index xxx rebuild重建索引global_index_id_037
--查看分区表（6000行）、普通表的数据量（500行）
select count(*) from test_ugi_037;
select count(*) from test_ugi_037_temp;
--查看执行计划，确认走index scan
explain analyse select * from test_ugi_037 where c_id = 2333;
--交换分区p4，破坏全局索引
alter table test_ugi_037 exchange partition (p4) with table test_ugi_037_temp;

--清理表
drop table test_ugi_037;
drop table test_ugi_037_temp;