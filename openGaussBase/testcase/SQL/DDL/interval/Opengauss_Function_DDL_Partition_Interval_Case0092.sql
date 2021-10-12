-- @testpoint: interval分区,ALTER TABLE MOVE PARTITION指定分区表的表空间，将分区移至其它表空间
drop table if exists my_ptb;
drop tablespace if exists tsp001;
drop tablespace if exists tsp002;

create tablespace tsp001 relative location 'partition_table_space/tsp001' maxsize '10m';
create tablespace tsp002 relative location 'partition_table_space/tsp002' maxsize '10m';
create table my_ptb(
col_1 smallint,
col_2 char(30),
col_3 int,
col_4 date,
col_5 boolean,
col_6 nchar(30),
col_7 float)
tablespace tsp001 partition by range (col_4) interval ('1 month')
(partition my_ptb_p1 values less than ('2020-03-01'),
partition my_ptb_p2 values less than ('2020-04-01'),
partition my_ptb_p3 values less than ('2020-05-01'));

insert into my_ptb values (1,'aaa',1,'2020-02-23',true,'aaa',1.1);
insert into my_ptb values (2,'bbb',2,'2020-03-23',false,'bbb',2.2);
insert into my_ptb values (3,'ccc',3,'2020-04-23',true,'ccc',3.3);
insert into my_ptb values (4,'ddd',4,'2020-05-23',false,'ddd',4.4);
insert into my_ptb values (5,'eee',5,'2020-06-23',true,'eee',5.5);

select relname, boundaries, spcname from pg_partition p join pg_tablespace t on p.reltablespace=t.oid
where p.parentid = (select oid from pg_class where relname = 'my_ptb') order by relname;

alter table my_ptb move partition my_ptb_p3 tablespace tsp002;
alter table my_ptb move partition sys_p1 tablespace tsp002;

select relname, boundaries, spcname from pg_partition p join pg_tablespace t on p.reltablespace=t.oid
where p.parentid = (select oid from pg_class where relname = 'my_ptb') order by relname;

drop table if exists my_ptb;
drop tablespace if exists tsp001;
drop tablespace if exists tsp002;