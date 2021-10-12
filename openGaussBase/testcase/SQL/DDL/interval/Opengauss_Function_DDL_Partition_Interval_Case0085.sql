-- @testpoint: interval分区,ALTER TABLE修改表分区名称，表不存在或者分区名不存在时合理报错
drop table if exists table8;

create table table8( 
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
	partition table8_p1 values less than ('2020-02-29')
);

-- 插入数据
insert into table8 values (1,'aaa',1,'2019-02-28',true,'aaa',1.1);
insert into table8 values (2,'bbb',2,'2020-02-28',false,'bbb',2.2);  --table8_p1
insert into table8 values (3,'ccc',3,'2020-02-29',true,'ccc',3.3);   --sys_p1
insert into table8 values (4,'ddd',4,'2021-02-28',false,'ddd',4.4);  --sys_p2

-- 查看分区表信息
select relname, parttype, partstrategy, boundaries,reltablespace from pg_partition
where parentid = (select oid from pg_class where relname = 'table8') order by relname;

-- 重命名时分区表不存在
alter table a_table_not_exist rename partition table8_p1 to table8_p2;
-- 重命名时扩展分区不存在
alter table table8 rename partition sys_p4 to table8_p3;

-- 查看分区表信息
select relname, parttype, partstrategy, boundaries,reltablespace from pg_partition
where parentid = (select oid from pg_class where relname = 'table8') order by relname;

drop table if exists table8;