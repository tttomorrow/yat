-- @testpoint: 分区表使用数据类型为jsonb的列创建主外键，合理报错

-- 分区表创建主键:分区键不为主键，且数据类型不为jsonb
drop table if exists tab1251;
create table tab1251(
col_1 smallint,
col_2 jsonb primary key,
col_3 int,
col_4 date not null,
col_5 jsonb,
col_6 nchar(30),
col_7 float
)
partition by range (col_4)
interval ('1 month')
(
	partition tab125_p1 values less than ('2020-03-01'),
	partition tab125_p2 values less than ('2020-04-01'),
	partition tab125_p3 values less than ('2020-05-01')
);

-- 分区表创建主键:分区键为主键，分区键数据类型为jsonb,合理报错
drop table if exists tab1252;
create table tab1252(
col_1 smallint,
col_2 jsonb primary key,
col_3 int,
col_4 date not null,
col_5 jsonb
)
partition by range (col_2)
(
	partition tab125_p1 values less than ('2021-03-01'),
	partition tab125_p2 values less than ('2022-04-01'),
	partition tab125_p3 values less than ('2023-05-01')
);

-- 分区表创建主键:分区键为主键，分区键数据类型不为jsonb
drop table if exists tab1253;
create table tab1253(
col_1 smallint,
col_2 jsonb,
col_3 int primary key,
col_4 date not null,
col_5 jsonb
)
partition by range (col_3)
(
	partition tab125_p1 values less than ('20210301'),
	partition tab125_p2 values less than ('20220401'),
	partition tab125_p3 values less than ('20230501')
);

--分区表创建主键:分区键数据类型为jsonb
drop table if exists tab1254;
drop table if exists tab1255;
create table tab1254(
col_1 smallint,
col_2 jsonb primary key,
col_3 int unique,
col_4 date not null,
col_5 jsonb
)
partition by range (col_3)
(
	partition tab125_p1 values less than ('20210301'),
	partition tab125_p2 values less than ('20220401'),
	partition tab125_p3 values less than ('20230501')
);

create table tab1255 (
col_1 int ,
col_2 jsonb primary key,
col_3 int  ,foreign key(col_2) references tab1254(col_2))
partition by range (col_3)
(
	partition tab125_p1 values less than ('20210301'),
	partition tab125_p2 values less than ('20220401'),
	partition tab125_p3 values less than ('20230501')
);

--清理数据

drop table if exists tab1251 cascade;
drop table if exists tab1252 cascade;
drop table if exists tab1253 cascade;
drop table if exists tab1254 cascade;
drop table if exists tab1255 cascade;