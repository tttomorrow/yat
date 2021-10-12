-- @testpoint: interval分区,ALTER TABLE修改表分区名称，包括预定义分区和扩展分区，查询旧分区信息时合理报错
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
insert into table8 values (1,'aaa',1,'2019-02-28',true,'aaa',1.1);  --table8_p1
insert into table8 values (2,'bbb',2,'2020-02-28',false,'bbb',2.2); --table8_p1
insert into table8 values (3,'ccc',3,'2020-02-29',true,'ccc',3.3);  --sys_p1
insert into table8 values (4,'ddd',4,'2021-02-28',false,'ddd',4.4);  --sys_p2
insert into table8 values (5,'eee',5,'2022-02-28',true,'eee',5.5);    --sys_p3
insert into table8 values (6,'fff',6,'2023-02-28',false,'fff',6.6);  --sys_p4
insert into table8 values (7,'fff',7,'2024-02-29',false,'fff',6.6);  --sys_p5

-- 查看分区表信息
select relname, parttype, partstrategy, boundaries,reltablespace from pg_partition
where parentid = (select oid from pg_class where relname = 'table8') order by relname;

-- 查看各分区中数据
select * from table8 partition (table8_p1)order by col_4;
select * from table8 partition (sys_p1)order by col_4;
select * from table8 partition (sys_p2)order by col_4;
select * from table8 partition (sys_p3)order by col_4;
select * from table8 partition (sys_p4)order by col_4;
select * from table8 partition (sys_p5)order by col_4;

-- 普通分区
alter table table8 rename partition table8_p1 to new_name1;
-- 扩展分区
alter table table8 rename partition sys_p5 to new_name2;
alter table table8 rename partition sys_p4 to new_name3;

-- 查看分区表信息
select relname, parttype, partstrategy, boundaries,reltablespace from pg_partition
where parentid = (select oid from pg_class where relname = 'table8') order by relname;

insert into table8 values (8,'fff',8,'2023-03-01',false,'fff',6.6);

-- 查看各分区中数据,被重命名的分区报错不存在
select * from table8 partition (table8_p1)order by col_4;
select * from table8 partition (sys_p1)order by col_4;
select * from table8 partition (sys_p2)order by col_4;
select * from table8 partition (sys_p3)order by col_4;
select * from table8 partition (sys_p4)order by col_4;
select * from table8 partition (sys_p5)order by col_4;
select * from table8 partition (new_name1)order by col_4;
select * from table8 partition (new_name2)order by col_4;
select * from table8 partition (new_name3)order by col_4;

drop table if exists table8;