-- @testpoint: interval分区,先插入数据生成自动分区，再创建分区表索引：LOCAL索引
drop index if exists pt_idx_001;
drop table if exists table1;

create table table1( 
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
	partition table1_p1 values less than ('2020-03-01'),
	partition table1_p2 values less than ('2020-04-01'),
	partition table1_p3 values less than ('2020-05-01')
);

insert into table1 values (1,'aaa',1,'2020-02-23',true,'aaa',1.1);
insert into table1 values (2,'bbb',2,'2020-03-23',false,'bbb',2.2);
insert into table1 values (3,'ccc',3,'2020-04-23',true,'ccc',3.3);
insert into table1 values (4,'ddd',4,'2020-05-23',false,'ddd',4.4);
insert into table1 values (5,'eee',5,'2020-06-23',true,'eee',5.5);
insert into table1 values (6,'fff',6,'2020-07-23',false,'fff',6.6);

create index pt_idx_001 on table1(col_4) local
(
    partition col_4_index1,
    partition col_4_index2,
    partition col_4_index3,
	partition col_4_index4,
    partition col_4_index5,
    partition col_4_index6
); 

insert into table1 values (6,'fff',6,'2020-08-23',false,'fff',6.6);

select relname, parttype, partstrategy, boundaries,reltablespace from pg_partition
where parentid = (select oid from pg_class where relname = 'table1') order by relname;
	
select relname, parttype, partstrategy, boundaries,reltablespace from pg_partition
where parentid = (select oid from pg_class where relname = 'pt_idx_001') order by relname;

drop index if exists pt_idx_001;
drop table if exists table1;