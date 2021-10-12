-- @testpoint: interval分区,EXCHANGE PARTITION普通表中的数据满足指定分区的分区键范围，指定WITHOUT VALIDATION
drop table if exists tb_c;
drop table if exists tb_p;
drop tablespace if exists tsp_1;
drop tablespace if exists tsp_2;

create tablespace tsp_1 relative location 'partition_table_space/tsp_1' maxsize '10m';
create tablespace tsp_2 relative location 'partition_table_space/tsp_2' maxsize '10m';

create table tb_p(c1 smallint,c2 char(30),c3 int,
c4 date not null,c5 boolean,c6 nchar(30),c7 float)
partition by range (c4)interval ('1 month')
(partition tb_p_p1 values less than ('2020-01-01') tablespace tsp_1);

create table tb_c(c1 smallint,c2 char(30),
c3 int,c4 date not null,c5 boolean,c6 nchar(30),
c7 float)tablespace tsp_2;

-- tb_p插入数据
insert into tb_p values (1,'aaa',1,'2019-12-31',true,'aaa',1.1);
insert into tb_p values (2,'bbb',2,'2020-01-01',false,'bbb',2.2);
insert into tb_p values (3,'ccc',3,'2020-02-01',true,'ccc',3.3);

-- tb_c插入数据
insert into tb_c values (2,'ggg',2,'2020-01-01',false,'ggg',2.2);

select relname, boundaries, spcname from pg_partition p join pg_tablespace t on p.reltablespace=t.oid
where p.parentid = (select oid from pg_class where relname = 'tb_p') order by relname;

-- 查看各分区中数据
select * from tb_p partition (tb_p_p1)order by c4;
select * from tb_p partition (sys_p1)order by c4;
select * from tb_p partition (sys_p2)order by c4;
select * from tb_c;

alter table tb_p exchange partition (sys_p1) with table tb_c without validation;

select * from tb_p partition (tb_p_p1)order by c4;
select * from tb_p partition (sys_p1)order by c4;
select * from tb_p partition (sys_p2)order by c4;
select * from tb_c;

select relname, boundaries, spcname from pg_partition p join pg_tablespace t on p.reltablespace=t.oid
where p.parentid = (select oid from pg_class where relname = 'tb_p') order by relname;

drop table if exists tb_p;
drop table if exists tb_c;
drop tablespace if exists tsp_1;
drop tablespace if exists tsp_2;