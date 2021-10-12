-- @testpoint: interval分区,ALTER TABLE DROP PARTITION删除仅有的分区，合理报错
drop table if exists my_ptb1;

create table my_ptb1(
col_1 smallint,
col_2 char(30),
col_3 int,
col_4 date,
col_5 boolean,
col_6 nchar(30),
col_7 float
)
partition by range (col_4) interval ('1 month')
(partition my_ptb1_p1 values less than ('2020-03-01'));

alter table my_ptb1 drop partition my_ptb1_p1;

insert into my_ptb1 values (4,'ddd',4,'2020-05-23',false,'ddd',4.4);
select relname, parttype, partstrategy, boundaries,reltablespace from pg_partition
where parentid = (select oid from pg_class where relname = 'my_ptb1') order by relname;
alter table my_ptb1 drop partition my_ptb1_p1;

alter table my_ptb1 drop partition sys_p1;

select relname, parttype, partstrategy, boundaries,reltablespace from pg_partition
where parentid = (select oid from pg_class where relname = 'my_ptb1') order by relname;

drop table if exists my_ptb1;