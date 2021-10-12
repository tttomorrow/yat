-- @testpoint: interval分区,EXCHANGE PARTITION普通表中的数据不满足指定分区的分区键范围，指定WITH VALIDATION,合理报错
drop table if exists par_tb;
drop table if exists com_tb;

create table par_tb(
col_1 smallint,
col_2 char(30),
col_3 int,
col_4 date not null,
col_5 boolean,
col_6 nchar(30),
col_7 float)
partition by range (col_4)interval ('1 month')
(partition par_tb_p1 values less than ('2020-01-01'));

create table com_tb(
col_1 smallint,
col_2 char(30),
col_3 int,
col_4 date not null,
col_5 boolean,
col_6 nchar(30),
col_7 float);

insert into par_tb values (1,'aaa',1,'2019-12-31',true,'aaa',1.1);
insert into com_tb values (1,'aaa',1,'2022-12-15',true,'aaa',1.1);
insert into com_tb values (1,'aaa',1,'2018-12-15',true,'aaa',1.1);

select * from par_tb partition (par_tb_p1)order by col_4;
select * from com_tb;

-- exchange partition
alter table par_tb exchange partition (par_tb_p1) with table com_tb with validation;

select * from par_tb partition (par_tb_p1)order by col_4;
select * from com_tb;

drop table if exists par_tb;
drop table if exists com_tb;