-- @testpoint: interval分区,预定义分区指定的表空间不在STORE IN列表中,自动扩展分区使用STORE IN中定义的表空间
drop table if exists table1;
drop tablespace if exists tsp1;
drop tablespace if exists tsp2;
drop tablespace if exists tsp3;
drop tablespace if exists tsp4;
drop tablespace if exists tsp5;
drop tablespace if exists tsp6;

create tablespace tsp1 relative location 'partition_table_space/tsp1' maxsize '10m';
create tablespace tsp2 relative location 'partition_table_space/tsp2' maxsize '10m';
create tablespace tsp3 relative location 'partition_table_space/tsp3' maxsize '10m';
create tablespace tsp4 relative location 'partition_table_space/tsp4' maxsize '10m';
create tablespace tsp5 relative location 'partition_table_space/tsp5' maxsize '10m';
create tablespace tsp6 relative location 'partition_table_space/tsp6' maxsize '10m';

create table table1(
col_1 smallint,
col_2 char(30),
col_3 int,
col_4 date,
col_5 boolean,
col_6 nchar(30),
col_7 float
)
partition by range (col_4)
interval ('1 month') store in(tsp1,tsp2,tsp3)
(
partition table1_p1 values less than ('2020-03-01') tablespace tsp4,
partition table1_p2 values less than ('2020-04-01') tablespace tsp5,
partition table1_p3 values less than ('2020-05-01') tablespace tsp6
);

select relname, parttype, partstrategy, boundaries from pg_partition
where parentid = (select oid from pg_class where relname = 'table1') order by relname;

select relname, boundaries, spcname from pg_partition p join pg_tablespace t on p.reltablespace=t.oid
where p.parentid = (select oid from pg_class where relname = 'table1') order by relname;

insert into table1 values (1,'aaa',1,'2020-02-23',true,'aaa',1.1);
insert into table1 values (2,'bbb',2,'2020-03-23',false,'bbb',2.2);
insert into table1 values (3,'ccc',3,'2020-04-23',true,'ccc',3.3);
insert into table1 values (4,'ddd',4,'2020-05-23',false,'ddd',4.4);
insert into table1 values (5,'eee',5,'2020-06-23',true,'eee',5.5);
insert into table1 values (6,'fff',6,'2020-07-23',false,'fff',6.6);

select relname, parttype, partstrategy, boundaries from pg_partition
where parentid = (select oid from pg_class where relname = 'table1') order by relname;

select relname, boundaries, spcname from pg_partition p join pg_tablespace t on p.reltablespace=t.oid
where p.parentid = (select oid from pg_class where relname = 'table1') order by relname;

drop table if exists table1;
drop tablespace if exists tsp1;
drop tablespace if exists tsp2;
drop tablespace if exists tsp3;
drop tablespace if exists tsp4;
drop tablespace if exists tsp5;
drop tablespace if exists tsp6;