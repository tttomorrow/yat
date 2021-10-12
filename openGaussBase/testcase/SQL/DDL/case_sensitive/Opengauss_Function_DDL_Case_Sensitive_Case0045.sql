--  @testpoint: --通过视图查看索引验证索引的大小写
drop table if exists false_2 cascade;
create table false_2(a int,b int);

create index wms ON false_2(B);
create index wms ON false_2(b);


select * from pg_indexes WHERE INDEXNAME='wms';
select * from pg_indexes WHERE INDEXNAME='WMS';

drop table if exists false_2 cascade;