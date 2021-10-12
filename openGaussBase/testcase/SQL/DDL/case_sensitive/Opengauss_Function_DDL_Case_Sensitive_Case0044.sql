--  @testpoint: 创建索引，验证索引名大小写敏感
drop table if exists false_2 cascade;
create table false_2(a int,b int);

create index ee on false_2(a);
create index EE on false_2(A);
create index wms ON false_2(B);
create index wms ON false_2(b);

drop table if exists false_2 cascade;