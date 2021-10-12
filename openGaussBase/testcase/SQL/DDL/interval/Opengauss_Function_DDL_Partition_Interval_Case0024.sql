-- @testpoint: interval分区,创建时声明like子句,源表是普通表,新表是分区表,指定INCLUDING CONSTRAINTS,违背约束时合理报错

drop table if exists common_table_001;
drop table if exists partition_table_001;

-- 创建普通表作为分区表like的源表
create table common_table_001( 
col_1 smallint primary key check (col_1 > 0),
col_2 char(30) default 'hey boy',
col_3 int unique,
col_4 date,
col_5 boolean, 
col_6 nchar(30) not null,
col_7 float
);

-- like指定INCLUDING CONSTRAINTS
create table partition_table_001( 
like common_table_001 including constraints)
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

-- 验证check项，合理报错
--（非空约束将总是复制到新表中，CHECK约束则仅在指定了INCLUDING CONSTRAINTS的时候才复制，
-- 而其他类型的约束则永远也不会被复制。此规则同时适用于表约束和列约束。）
insert into partition_table_001 values (3,'ccc',3,'2018-04-23',true,null,3.3);
insert into partition_table_001 values (-3,'ccc',3,'2018-04-23',true,'ccc',3.3);
select * from partition_table_001;

drop table if exists common_table_001;
drop table if exists partition_table_001;