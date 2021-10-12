-- @testpoint: interval分区,update时存在需要行迁移的情况,不指定行迁移开关,默认行迁移开关打开
drop table if exists table1;

create table table1(
col_1 smallint default 10,
col_2 char(30),
col_3 int,
col_4 date not null,
col_5 boolean,
col_6 nchar(30),
col_7 float
)
partition by range (col_4)
interval ('1 day')
(
        partition table1_p1 values less than ('2000-01-01')
);

begin
        for i in 1..10 loop
          insert into table1(col_4) select date '1999-12-31' + i ;
        end loop;
end;
/

select relname, parttype, partstrategy, boundaries, reltablespace, intervaltablespace, interval, transit
from pg_partition where parentid = (select oid from pg_class where relname = 'table1') order by relname;

update table1 set col_4='2000-01-09' where col_1=10;

select * from table1 partition (table1_p1)order by col_4;
select * from table1 partition (sys_p1)order by col_4;
select * from table1 partition (sys_p2)order by col_4;
select * from table1 partition (sys_p3)order by col_4;
select * from table1 partition (sys_p4)order by col_4;
select * from table1 partition (sys_p5)order by col_4;
select * from table1 partition (sys_p6)order by col_4;
select * from table1 partition (sys_p7)order by col_4;
select * from table1 partition (sys_p8)order by col_4;
select * from table1 partition (sys_p9)order by col_4;
select * from table1 partition (sys_p10)order by col_4;

drop table if exists table1;