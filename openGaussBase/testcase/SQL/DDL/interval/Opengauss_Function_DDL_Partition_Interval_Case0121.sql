-- @testpoint: interval分区,MERGE PARTITIONS不同表空间内多个预定义分区与扩展分区合并
drop table if exists pt2;
drop tablespace if exists utsp1;
drop tablespace if exists utsp2;
drop tablespace if exists utsp3;
drop tablespace if exists utsp4;
drop tablespace if exists utsp5;
drop tablespace if exists utsp6;

create tablespace utsp1 relative location 'partition_table_space/utsp1' maxsize '10m';
create tablespace utsp2 relative location 'partition_table_space/utsp2' maxsize '10m';
create tablespace utsp3 relative location 'partition_table_space/utsp3' maxsize '10m';
create tablespace utsp4 relative location 'partition_table_space/utsp4' maxsize '10m';
create tablespace utsp5 relative location 'partition_table_space/utsp5' maxsize '10m';
create tablespace utsp6 relative location 'partition_table_space/utsp6' maxsize '10m';

create table pt2(
col_1 smallint,
col_2 char(30),
col_3 int,
col_4 date,
col_5 boolean,
col_6 nchar(30),
col_7 float
)
partition by range (col_4)
interval ('1 month') store in(utsp1,utsp2,utsp3)
(
partition pt2_p1 values less than ('2020-03-01') tablespace utsp4,
partition pt2_p2 values less than ('2020-04-01') tablespace utsp5,
partition pt2_p3 values less than ('2020-05-01') tablespace utsp6
);

-- 插入数据
insert into pt2 values (1,'aaa',1,'2020-02-23',true,'aaa',1.1);
insert into pt2 values (2,'bbb',2,'2020-03-23',false,'bbb',2.2);
insert into pt2 values (3,'ccc',3,'2020-04-23',true,'ccc',3.3);
insert into pt2 values (4,'ddd',4,'2020-05-23',false,'ddd',4.4);
insert into pt2 values (5,'eee',5,'2020-06-23',true,'eee',5.5);
insert into pt2 values (6,'fff',6,'2020-07-23',false,'fff',6.6);

-- 查看分区信息
select relname, boundaries, spcname from pg_partition p join pg_tablespace t on p.reltablespace=t.oid
where p.parentid = (select oid from pg_class where relname = 'pt2') order by relname;

alter table pt2 merge partitions pt2_p1, pt2_p2 into partition new1;
alter table pt2 merge partitions pt2_p3, sys_p1 into partition new2;
alter table pt2 merge partitions sys_p2, sys_p3 into partition new3;

-- 查看分区信息
select relname, boundaries, spcname from pg_partition p join pg_tablespace t on p.reltablespace=t.oid
where p.parentid = (select oid from pg_class where relname = 'pt2') order by relname;

insert into pt2 values (8,'fff',8,'2020-03-15',false,'fff',8.8);
insert into pt2 values (9,'fff',9,'2020-05-15',false,'fff',9.9);
insert into pt2 values (10,'fff',10,'2020-08-15',false,'fff',9.9);

-- 查看分区信息
select relname, boundaries, spcname from pg_partition p join pg_tablespace t on p.reltablespace=t.oid
where p.parentid = (select oid from pg_class where relname = 'pt2') order by relname;

-- 查看各分区中数据
select * from pt2 partition (sys_p1)order by col_4;
select * from pt2 partition (new1)order by col_4;
select * from pt2 partition (new2)order by col_4;
select * from pt2 partition (new3)order by col_4;

drop table if exists pt2;
drop tablespace if exists utsp1;
drop tablespace if exists utsp2;
drop tablespace if exists utsp3;
drop tablespace if exists utsp4;
drop tablespace if exists utsp5;
drop tablespace if exists utsp6;