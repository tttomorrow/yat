-- @testpoint: interval分区,EXCHANGE PARTITION分区表和普通表压缩信息不一致，合理报错
drop table if exists pt1;
drop table if exists common_table1;

create table pt1(
col_1 smallint,
col_2 char(30),
col_3 int,
col_4 date not null,
col_5 boolean,
col_6 nchar(30),
col_7 float
)
partition by range (col_4)
interval ('1 month')
(
partition pt1_p1 values less than ('2020-01-01'));

create table common_table1(
col_1 smallint,
col_2 char(30),
col_3 int,
col_4 date not null,
col_5 boolean,
col_6 nchar(30),
col_7 float
)with (orientation = column, compression=high);

insert into pt1 values (1,'aaa',1,'2019-12-31',true,'aaa',1.1);
insert into common_table1 values (1,'aaa',1,'2019-12-15',true,'aaa',1.1);

alter table pt1 exchange partition (pt1_p1) with table common_table1;

drop table if exists pt1;
drop table if exists common_table1;