-- @testpoint: 创建list分区表使用values in
--step1:创建list分区表，使用values in;expect:成功
drop table if exists tb_plugin0009;
create table tb_plugin0009 (col1 int, col2 text(10),col3 double)
partition by list(col1)
(
partition p1 values in (2000),
partition p2 values in (3000),
partition p3 values in (4000),
partition p4 values in (5000)
)enable row movement;

--step2:插入数据;expect:成功
insert into tb_plugin0009 values(2000,'分区1',456.568),(3000,'分区2',456.568),(4000,'分区3',56.568);

--step3:增加分区;expect:成功
alter table tb_plugin0009 add partition p5 values (6000);

--step4:查看分区;expect:成功
select t1.relname, partstrategy, boundaries from pg_partition t1, pg_class t2 where t1.parentid = t2.oid and t2.relname = 'tb_plugin0009' and t1.parttype = 'p' order by relname asc;

--step5:删除字段;expect:成功
alter table tb_plugin0009 drop column if exists col3;

--step6:查看分区，分区数不变;expect:成功
select t1.relname, partstrategy, boundaries from pg_partition t1, pg_class t2 where t1.parentid = t2.oid and t2.relname = 'tb_plugin0009' and t1.parttype = 'p' order by relname asc;

--step7:删除分区;expect:成功
alter table tb_plugin0009 drop partition p1;

--step8:查看分区，无p1分区;expect:成功
select t1.relname, partstrategy, boundaries from pg_partition t1, pg_class t2 where t1.parentid = t2.oid and t2.relname = 'tb_plugin0009' and t1.parttype = 'p' order by relname asc;

--step9:创建list分区表，使用values;expect:成功
drop table if exists tb_plugin0009_01;
create table tb_plugin0009_01 (col1 int, col2 text(10),col3 double)
partition by list(col1)
(
partition p1 values (2000),
partition p2 values (3000),
partition p3 values (4000),
partition p4 values (5000)
)enable row movement;

--step10:清理环境;expect:成功
drop table if exists tb_plugin0009;
drop table if exists tb_plugin0009_01;


