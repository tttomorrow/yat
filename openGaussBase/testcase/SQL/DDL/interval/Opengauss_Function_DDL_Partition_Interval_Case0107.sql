-- @testpoint: interval分区,EXCHANGE PARTITION交换后普通表和分区的表空间信息同时被置换
drop table if exists par_tb;
drop table if exists com_tb;
drop tablespace if exists mytsp111;
drop tablespace if exists mytsp222;

create tablespace mytsp111 relative location 'partition_table_space/mytsp111' maxsize '10m';
create tablespace mytsp222 relative location 'partition_table_space/mytsp222' maxsize '10m';

create table par_tb(
col_1 smallint,
col_2 char(30),
col_3 int,
col_4 date not null,
col_5 boolean,
col_6 nchar(30),
col_7 float
)
partition by range (col_4)interval ('1 month')
(partition par_tb_p1 values less than ('2020-01-01') tablespace mytsp111);

create table com_tb(
col_1 smallint,
col_2 char(30),
col_3 int,
col_4 date not null,
col_5 boolean,
col_6 nchar(30),
col_7 float
)tablespace mytsp222;

insert into par_tb values (1,'aaa',1,'2019-12-31',true,'aaa',1.1);
insert into com_tb values (1,'aaa',1,'2019-12-15',true,'aaa',1.1);

-- 查询交换前表空间
select relname, boundaries, spcname from pg_partition p join pg_tablespace t on p.reltablespace=t.oid
where p.parentid = (select oid from pg_class where relname = 'par_tb') order by relname;
select tablespace from pg_tables where tablename = 'com_tb';

select * from par_tb partition (par_tb_p1)order by col_4;
select * from com_tb;

-- exchange partition
alter table par_tb exchange partition (par_tb_p1) with table com_tb;

select * from par_tb partition (par_tb_p1)order by col_4;
select * from com_tb;

-- 查询交换后表空间
select relname, boundaries, spcname from pg_partition p join pg_tablespace t on p.reltablespace=t.oid
where p.parentid = (select oid from pg_class where relname = 'par_tb') order by relname;
select tablespace from pg_tables where tablename = 'com_tb';

drop table if exists par_tb;
drop table if exists com_tb;
drop tablespace if exists mytsp111;
drop tablespace if exists mytsp222;