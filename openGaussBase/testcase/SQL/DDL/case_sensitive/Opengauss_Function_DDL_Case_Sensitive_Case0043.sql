--  @testpoint: 创建索引，验证表名字段名
drop table if exists false_2 cascade;
create table false_2(a int,b int);

create index yy on FALSE_2(a);
create index YY on false_2(B);

drop table if exists false_2 cascade;
