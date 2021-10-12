-- @testpoint: 分区表使用数据类型为jsonb的列创建索引，合理报错

--建分区表
drop table if exists tab121;
create table tab121(
col_1 smallint,
col_2 jsonb,
col_3 int,
col_4 date not null,
col_5 jsonb,
col_6 nchar(30),
col_7 float
)
partition by range (col_4)
interval ('1 month')
(
	partition tab121_p1 values less than ('2020-03-01'),
	partition tab121_p2 values less than ('2020-04-01'),
	partition tab121_p3 values less than ('2020-05-01')
);

-- 分区表local索引
drop index if exists index1211;
create index index1211 on tab121(col_2) local;
create unique index index1212 on tab121 using btree(col_5 asc)local;

-- 分区表local索引:不支持gin，gist索引，合理报错
create  index index12120 on tab121 using gin(col_4 asc)local;
create  index index12120 on tab121 using gist(col_4 asc)local;

-- 分区表global索引仅支持btree索引
create unique index index1213 on tab121 using btree(col_5 asc);
create unique index index1214 on tab121 using btree(col_5 asc)global;
create unique index unique_index1215 on tab121 using btree(col_5 asc)global;

-- 分区表global索引:不支持gin索引，且local索引和global索引不能为为同一列，合理报错
create index index1216 on tab121 using gin(col_5)global;
create unique index index1217 on tab121 using btree(col_2 asc)local;

--jsonb类型的列不能作为分区键，也不支持gist索引，故合理报错
create unique index index1218 on tab121 using btree(col_5 asc)local;
create index index1219 on tab121 using gist(col_2)local;

--清理数据
drop index if exists index1211;
drop index if exists index1212;
drop index if exists index1213;
drop index if exists index1214;
drop index if exists index1215;
drop index if exists index1216;
drop index if exists index1217;
drop index if exists index1218;
drop index if exists index1219;
drop table if exists tab121;