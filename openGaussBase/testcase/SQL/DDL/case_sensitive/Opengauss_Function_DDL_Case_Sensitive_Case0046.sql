--  @testpoint: 删除索引验证索引的大小写
drop table if exists false_2 cascade;
create table false_2(a int,b int);

create index wms ON false_2(B);

create index yy on FALSE_2(a);


drop index  WMS;
drop index wms;
drop index yy;
drop index YY;
drop table false_2 cascade;