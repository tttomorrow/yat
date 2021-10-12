-- @testpoint: interval分区,MERGE PARTITIONS分区表带索引，合并后会保留上边界分区的索引，其余索引删除
drop table if exists pt5;

create table pt5( 
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
(   partition pt5_p1 values less than ('2020-03-01'),
    partition pt5_p2 values less than ('2020-04-01'),
    partition pt5_p3 values less than ('2020-05-01'));

create index partiton_table_index_001 on pt5(col_4) local; 

-- 插入的分区键值
insert into pt5 values (1,'aaa',1,'2020-02-23',true,'aaa',1.1);
insert into pt5 values (2,'bbb',2,'2020-03-23',false,'bbb',2.2);
insert into pt5 values (3,'ccc',3,'2020-04-23',true,'ccc',3.3);
insert into pt5 values (4,'ddd',4,'2020-05-23',false,'ddd',4.4);
insert into pt5 values (5,'eee',5,'2020-06-23',true,'eee',5.5);
insert into pt5 values (6,'fff',6,'2020-07-23',false,'fff',6.6);

-- 查看分区表、分区表索引信息
select relname, parttype, partstrategy, boundaries,reltablespace from pg_partition
where parentid = (select oid from pg_class where relname = 'pt5')
order by relname;

select relname, parttype, partstrategy, boundaries,reltablespace from pg_partition
where parentid = (select oid from pg_class where relname = 'partiton_table_index_001')
order by relname;

alter table pt5 merge partitions pt5_p1, pt5_p2 into partition new_1;
alter table pt5 merge partitions pt5_p3, sys_p1 into partition new_2;
alter table pt5 merge partitions sys_p2, sys_p3 into partition new_3;

-- 查看分区表、分区表索引信息
select relname, parttype, partstrategy, boundaries,reltablespace from pg_partition
where parentid = (select oid from pg_class where relname = 'pt5') order by relname;

select relname, parttype, partstrategy, boundaries,reltablespace from pg_partition
where parentid = (select oid from pg_class where relname = 'partiton_table_index_001') order by relname;

insert into pt5 values (8,'fff',8,'2020-03-15',false,'fff',8.8);
insert into pt5 values (9,'fff',9,'2020-05-15',false,'fff',9.9);
insert into pt5 values (10,'fff',10,'2020-08-15',false,'fff',9.9);

-- 查看分区表、分区表索引信息
select relname, parttype, partstrategy, boundaries,reltablespace from pg_partition
where parentid = (select oid from pg_class where relname = 'pt5') order by relname;

select relname, parttype, partstrategy, boundaries,reltablespace from pg_partition
where parentid = (select oid from pg_class where relname = 'partiton_table_index_001') order by relname;

drop table if exists pt5 cascade;