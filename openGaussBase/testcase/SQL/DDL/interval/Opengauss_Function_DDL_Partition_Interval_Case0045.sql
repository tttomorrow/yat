-- @testpoint: interval分区,某分区指定的表空间空间不足，再插入数据到该分区时合理报错
drop table if exists table1;
drop tablespace if exists tsp1;

create tablespace tsp1 relative location 'partition_table_space/tsp1' maxsize '5k';

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
interval ('1 month') 
(
partition table1_p1 values less than ('2020-03-01') tablespace tsp1,
partition table1_p2 values less than ('2020-04-01'),
partition table1_p3 values less than ('2020-05-01')
);

select relname, parttype, partstrategy, boundaries from pg_partition
where parentid = (select oid from pg_class where relname = 'table1')
order by relname;

select relname, boundaries, spcname from pg_partition p join pg_tablespace t on p.reltablespace=t.oid 
where p.parentid = (select oid from pg_class where relname = 'table1') order by relname;

insert into table1 values (1,'aaa',1,'2020-02-23',true,'aaa',1.1);

drop table if exists table1;
drop tablespace if exists tsp1;