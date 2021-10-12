--  @testpoint: --子查询验证表名大小写
drop table if exists WMS cascade;
drop table if exists wms cascade;
create table wms(A int,b char(10));
insert into wms values(5,'re');
insert into wms values(3,'aa');
insert into wms values(5,'xx');
select * from false_1 a where a.a in (select a from WMS);
select * from false_1 a where a.a in (select a from wms);