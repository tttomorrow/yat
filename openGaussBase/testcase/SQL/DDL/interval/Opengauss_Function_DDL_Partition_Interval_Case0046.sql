-- @testpoint: interval分区,向扩展分区插入数据将store in中表空间占满再插入数据失败合理报错,向预定义分区插入数据不受影响
drop table if exists table1;
drop tablespace if exists tsp1;
drop tablespace if exists tsp2;
drop tablespace if exists tsp3;

create tablespace tsp1 relative location 'partition_table_space/tsp1' maxsize '1m';
create tablespace tsp2 relative location 'partition_table_space/tsp2' maxsize '1m';
create tablespace tsp3 relative location 'partition_table_space/tsp3' maxsize '1m';

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
interval ('1 day') store in(tsp1,tsp2,tsp3)
(
	partition table1_p1 values less than ('2020-03-01')
);

select relname, parttype, partstrategy, boundaries from pg_partition
where parentid = (select oid from pg_class where relname = 'table1') order by relname;

select relname, boundaries, spcname from pg_partition p join pg_tablespace t on p.reltablespace=t.oid
where p.parentid = (select oid from pg_class where relname = 'table1') order by relname;

-- 先插入数据，不匹配预定义分区，产生自动扩展分区，使用的时store in中的第一个表空间tps1
begin
	for i in 1..1100 loop
	  insert into table1(col_4) select date '2020-03-01' + i ;
	end loop;
end;
/
-- 再插入数据到预定义分区
begin
	for i in 1..1000 loop
	  insert into table1(col_4) select date '1920-03-01' + i ;
	end loop;
end;
/

select relname, parttype, partstrategy, boundaries,reltablespace from pg_partition
where parentid = (select oid from pg_class where relname = 'table1') order by relname;

drop table if exists table1;
drop tablespace if exists tsp1;
drop tablespace if exists tsp2;
drop tablespace if exists tsp3;