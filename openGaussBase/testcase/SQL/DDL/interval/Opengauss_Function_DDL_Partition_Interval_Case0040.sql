-- @testpoint: interval分区,预定义分区指定表空间，未指定的分区存放再默认表空间
drop table if exists partiton_table_001;
drop tablespace if exists tsp1;

create tablespace tsp1 relative location 'partition_table_space/tsp1' maxsize '10m';

create table partiton_table_001(
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
partition partiton_table_001_p1 values less than ('2020-03-01') tablespace tsp1,
partition partiton_table_001_p2 values less than ('2020-04-01') tablespace tsp1,
partition partiton_table_001_p3 values less than ('2020-05-01')
);

select relname, parttype, partstrategy, boundaries from pg_partition
where parentid = (select oid from pg_class where relname = 'partiton_table_001')
order by relname;

select relname, boundaries, spcname from pg_partition p join pg_tablespace t on p.reltablespace=t.oid
where p.parentid = (select oid from pg_class where relname = 'partiton_table_001') order by relname;

insert into partiton_table_001 values (1,'aaa',1,'2020-02-23',true,'aaa',1.1);
insert into partiton_table_001 values (2,'bbb',2,'2020-03-23',false,'bbb',2.2);
insert into partiton_table_001 values (3,'ccc',3,'2020-04-23',true,'ccc',3.3);
insert into partiton_table_001 values (4,'ddd',4,'2020-05-23',false,'ddd',4.4);
insert into partiton_table_001 values (5,'eee',5,'2020-06-23',true,'eee',5.5);
insert into partiton_table_001 values (6,'fff',6,'2020-07-23',false,'fff',6.6);

select relname, parttype, partstrategy, boundaries from pg_partition
where parentid = (select oid from pg_class where relname = 'partiton_table_001')
order by relname;

select relname, boundaries, spcname from pg_partition p join pg_tablespace t on p.reltablespace=t.oid
where p.parentid = (select oid from pg_class where relname = 'partiton_table_001') order by relname;

drop table if exists partiton_table_001;
drop tablespace if exists tsp1;