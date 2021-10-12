-- @testpoint: interval分区,创建时声明like子句,源表是普通表,新表是分区表,指定INCLUDING INDEXES,违背唯一约束合理报错

drop table if exists common_table_001;
drop table if exists partition_table_001;

-- 创建普通表作为分区表like的源表
create table common_table_001(
col_1 smallint primary key check (col_1 > 0),
col_2 char(30) default 'hey boy',
col_3 int unique,
col_4 date,
col_5 boolean,
col_6 nchar(30),
col_7 float
)with(fillfactor=70);
create unique index idx_001 on common_table_001(col_4);

-- like指定INCLUDING INDEXES
create table partition_table_001(
like common_table_001 including indexes)
partition by range (col_4)
interval ('1 year')
(
	partition partition_p1 values less than ('2018-01-01'),
	partition partition_p2 values less than ('2019-01-01'),
	partition partition_p3 values less than ('2020-01-01')
);

-- 查看分区信息
select relname, parttype, partstrategy, boundaries,reltablespace from pg_partition
where parentid = (select oid from pg_class where relname = 'partition_table_001')
order by relname;

-- 验证索引，唯一索引被继承
insert into partition_table_001 values (5,'eee',5,'2020-06-23',true,'eee',5.5);
insert into partition_table_001 values (6,'fff',6,'2020-06-23',false,'fff',6.6);

drop table if exists common_table_001;
drop table if exists partition_table_001;