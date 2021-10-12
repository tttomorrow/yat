-- @testpoint: interval分区,带模式名删除表指定CASCADE | RESTRICT,存在依赖对象时RESTRICT合理报错
drop table if exists test9;
drop schema if exists xhy;
drop view if exists winners;

create schema xhy;
create table xhy.test9(col_4 date not null)
partition by range (col_4) interval ('1 month')
(partition test9_p1 values less than ('2020-01-01'));

create index on xhy.test9(col_4);
create view winners as select col_4 from xhy.test9;

drop table xhy.test9 restrict;
drop table xhy.test9 cascade;
drop schema xhy;