-- @testpoint: 验证【间隔】分区表【truncate partition】时，update global index关键字对【btree】类型【多字段索引】的重建作用

--创建分区表，插入样例数据，建立全局索引
drop table if exists test_ugi_050;
create table test_ugi_050
(
    c_id integer not null,
    c_date DATE,
    c_info varchar(20) not null
)
partition by range(c_date)
interval('2 day')
(
    partition p1 values less than ('2021-06-01 00:00:00'),
    partition p2 values less than ('2021-06-03 00:00:00'),
    partition p3 values less than ('2021-06-05 00:00:00'),
    partition p4 values less than ('2021-06-07 00:00:00'),
    partition p5 values less than ('2021-06-09 00:00:00')
);

insert into test_ugi_050(c_id, c_date, c_info) values(1, '2021-05-30 00:00:00', '1-1');
insert into test_ugi_050(c_id, c_date, c_info) values(2, '2021-05-31 00:00:00', '1-1');
insert into test_ugi_050(c_id, c_date, c_info) values(3, '2021-06-01 00:00:00', '1-1');
insert into test_ugi_050(c_id, c_date, c_info) values(4, '2021-06-02 00:00:00', '1-2');
insert into test_ugi_050(c_id, c_date, c_info) values(5, '2021-06-03 00:00:00', '1-2');
insert into test_ugi_050(c_id, c_date, c_info) values(6, '2021-06-04 00:00:00', '1-3');
insert into test_ugi_050(c_id, c_date, c_info) values(7, '2021-06-05 00:00:00', '1-3');
insert into test_ugi_050(c_id, c_date, c_info) values(8, '2021-06-06 00:00:00', '1-4');
insert into test_ugi_050(c_id, c_date, c_info) values(9, '2021-06-07 00:00:00', '1-4');
insert into test_ugi_050(c_id, c_date, c_info) values(10, '2021-06-08 00:00:00', '1-5');

create index global_index_id_050 on test_ugi_050(c_id, c_date) global;
create index global_index_info_050 on test_ugi_050(c_id, c_info) global;

--收集统计信息
analyse test_ugi_050;

--禁用seq scan，原因是初始数据量较小，因此禁用seq scan，验证是否会走到index scan
set enable_seqscan = off;

--确认清空分区可以破坏全局索引，并使用alter index xxx rebuild重建索引global_index_id_050
--查看分区状态
select t1.relname, partstrategy, boundaries from pg_partition t1, pg_class t2
where t1.parentid = t2.oid and t2.relname = 'test_ugi_050' and t1.parttype = 'p' order by relname;
--查看执行计划，确认走index scan
explain analyse select * from test_ugi_050 where c_date = '2021-06-01 00:00:00';
--清空分区p2，破坏全局索引
alter table test_ugi_050 truncate partition p2;
--分区p2已被清空
select t1.relname, partstrategy, boundaries from pg_partition t1, pg_class t2
where t1.parentid = t2.oid and t2.relname = 'test_ugi_050' and t1.parttype = 'p' order by relname;
--查看索引可用情况，索引已不可用
select c.relname, i.indisusable from pg_index i join pg_class c on i.indexrelid = c.oid 
where i.indrelid = 'test_ugi_050'::regclass order by c.relname;
--查看执行计划，走seq scan
explain analyse select * from test_ugi_050 where c_date = '2021-06-01 00:00:00';
--使用alter index xxx rebuild重建索引
alter index global_index_id_050 rebuild;
--查看索引可用情况，global_index_id_050可用，global_index_info_050不可用，可用索引查看执行计划确走index scan
select c.relname, i.indisusable from pg_index i join pg_class c on i.indexrelid = c.oid 
where i.indrelid = 'test_ugi_050'::regclass order by c.relname;
explain analyse select * from test_ugi_050 where c_date = '2021-06-03 00:00:00';
vacuum analyse;

--清空分区p3，破坏全局索引，带update global index关键字
alter table test_ugi_050 truncate partition p3 update global index;
--分区p3已被清空
select t1.relname, partstrategy, boundaries from pg_partition t1, pg_class t2
where t1.parentid = t2.oid and t2.relname = 'test_ugi_050' and t1.parttype = 'p' order by relname;
--此时，global_index_id_050可用，global_index_info_050不可用
select c.relname, i.indisusable from pg_index i join pg_class c on i.indexrelid = c.oid 
where i.indrelid = 'test_ugi_050'::regclass order by c.relname;
--查看执行计划，c_date走index scan，c_info走seq scan
explain analyse select * from test_ugi_050 where c_date = '2021-06-06 00:00:00';
explain analyse select * from test_ugi_050 where c_info = '1-4';

--表test_ugi_050应当包含"wait_clean_gpi=y"
select a.relname,a.parttype,a.reloptions from pg_partition a, pg_class b 
where a.parentid = b.oid and b.relname = 'test_ugi_050' and a.reloptions[3] like '%wait_clean_gpi=y%' order by 1,2,3;
--执行清理
vacuum analyse;
--表test_ugi_050不再包含"wait_clean_gpi=y"
select a.relname,a.parttype,a.reloptions from pg_partition a, pg_class b 
where a.parentid = b.oid and b.relname = 'test_ugi_050' and a.reloptions[3] like '%wait_clean_gpi=y%' order by 1,2,3;

--执行insert、update、delete等操作
insert into test_ugi_050(c_id, c_date, c_info) values(11, '2021-06-09 00:00:00', '1-5');
update test_ugi_050 set c_info = '4-1' where c_date = '2021-06-06 00:00:00';
delete from test_ugi_050 where c_date = '2021-06-09 00:00:00';
--查看执行计划，c_date走index scan
explain analyse select * from test_ugi_050 where c_date = '2021-06-06 00:00:00';

--确认test_ugi_050表中数据量正确，6行
select count(*) from test_ugi_050;
--清理表
drop table test_ugi_050;
--启用seq_scan
set enable_seqscan = on;