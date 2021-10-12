-- @testpoint: interval分区,ENABLE ROW MOVEMET，UPDATE后元组所在分区发生变化
drop table if exists ptb;

create table ptb(
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
partition ptb_p1 values less than ('2020-01-01')
);

-- 插入数据
insert into ptb values (1,'aaa',1,'2019-12-31',true,'aaa',1.1);
insert into ptb values (2,'bbb',2,'2020-01-01',false,'bbb',2.2);
insert into ptb values (3,'ccc',3,'2020-02-01',true,'ccc',3.3);
insert into ptb values (4,'ddd',4,'2020-03-01',false,'ddd',4.4);
insert into ptb values (5,'eee',5,'2020-04-01',true,'eee',5.5);

-- 查看分区表信息
select relname, parttype, partstrategy, boundaries,reltablespace,intervaltablespace,interval,transit
from pg_partition where parentid = (select oid from pg_class where relname = 'ptb') order by relname;

-- 查看各分区中数据
select * from ptb partition (ptb_p1)order by col_4;
select * from ptb partition (sys_p1)order by col_4;
select * from ptb partition (sys_p2)order by col_4;
select * from ptb partition (sys_p3)order by col_4;
select * from ptb partition (sys_p4)order by col_4;

alter table ptb enable row movement;

-- 更新数据落在原分区,更新成功
update ptb set col_4='2020-02-15' where col_4='2020-02-01';

-- 更新数据落在其他分区,更新成功
update ptb set col_4='2020-05-01' where col_4='2020-01-01';

-- 查看各分区中数据
select * from ptb partition (ptb_p1)order by col_4;
select * from ptb partition (sys_p1)order by col_4;
select * from ptb partition (sys_p2)order by col_4;
select * from ptb partition (sys_p3)order by col_4;
select * from ptb partition (sys_p4)order by col_4;
select * from ptb partition (sys_p5)order by col_4;

drop table if exists ptb;