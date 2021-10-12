-- @testpoint: interval分区,MERGE PARTITIONS同一表空间内预定义分区与扩展分区合并
drop table if exists pttb;

create table pttb(
col_1 smallint,
col_2 char(30),
col_3 int,
col_4 date,
col_5 boolean,
col_6 nchar(30),
col_7 float
)
partition by range (col_4) interval ('1 month')
(
partition pttb_p1 values less than ('2020-03-01'),
partition pttb_p2 values less than ('2020-04-01'),
partition pttb_p3 values less than ('2020-05-01'));

-- 查看分区信息
select relname, parttype, partstrategy, boundaries,reltablespace from pg_partition
where parentid = (select oid from pg_class where relname = 'pttb') order by relname;

-- 插入数据
insert into pttb values (1,'aaa',1,'2020-02-23',true,'aaa',1.1);  --pttb_p1
insert into pttb values (2,'bbb',2,'2020-03-23',false,'bbb',2.2); --pttb_p2
insert into pttb values (3,'ccc',3,'2020-04-23',true,'ccc',3.3);  --pttb_p3
insert into pttb values (4,'ddd',4,'2020-05-23',false,'ddd',4.4); --sys_p1
insert into pttb values (5,'eee',5,'2020-06-23',true,'eee',5.5);  --sys_p2
insert into pttb values (6,'fff',6,'2020-07-23',false,'fff',6.6); --sys_p3

-- 查看分区信息
select relname, parttype, partstrategy, boundaries,reltablespace from pg_partition
where parentid = (select oid from pg_class where relname = 'pttb') order by relname;

-- merge partitions
alter table pttb merge partitions pttb_p3,sys_p1, sys_p2, sys_p3 into partition pttb_p4;

-- 查看分区信息
select relname, parttype, partstrategy, boundaries,reltablespace from pg_partition
where parentid = (select oid from pg_class where relname = 'pttb') order by relname;

drop table if exists pttb;