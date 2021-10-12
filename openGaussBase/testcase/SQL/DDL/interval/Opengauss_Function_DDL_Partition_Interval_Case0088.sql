-- @testpoint: interval分区,ALTER TABLE修改表分区名称后,分区上索引名不会同步修改
drop index if exists mytbindex_001;
drop table if exists mytb001;

create table mytb001( 
col_1 smallint,
col_2 char(30),
col_3 int,
col_4 date,
col_5 boolean, 
col_6 nchar(30),
col_7 float
)
partition by range (col_4)
interval ('1 month') 
(
partition mytb001_p1 values less than ('2020-03-01'),
partition mytb001_p2 values less than ('2020-04-01'),
partition mytb001_p3 values less than ('2020-05-01')
);

create index mytbindex_001 on mytb001(col_4) local;

insert into mytb001 values (1,'aaa',1,'2020-02-23',true,'aaa',1.1);
insert into mytb001 values (2,'bbb',2,'2020-03-23',false,'bbb',2.2);
insert into mytb001 values (3,'ccc',3,'2020-04-23',true,'ccc',3.3);
insert into mytb001 values (4,'ddd',4,'2020-05-23',false,'ddd',4.4);
insert into mytb001 values (5,'eee',5,'2020-06-23',true,'eee',5.5);
insert into mytb001 values (6,'fff',6,'2020-07-23',false,'fff',6.6);

select relname, parttype, partstrategy, boundaries from pg_partition
where parentid = (select oid from pg_class where relname = 'mytb001') order by relname;

select relname, parttype, partstrategy, boundaries, indisusable from pg_partition where 
parentid = (select oid from pg_class where relname = 'mytbindex_001') order by relname;

alter table mytb001 rename partition mytb001_p1 to mytb001_p4;
alter table mytb001 rename partition sys_p1 to sys_p4;

select relname, parttype, partstrategy, boundaries from pg_partition
where parentid = (select oid from pg_class where relname = 'mytb001') order by relname;

select relname, parttype, partstrategy, boundaries, indisusable from pg_partition where 
parentid = (select oid from pg_class where relname = 'mytbindex_001') order by relname;

drop index if exists mytbindex_001;
drop table if exists mytb001;