-- @testpoint: 创建视图时使用to_clob类型转换函数

drop table if exists test2;
create table test2 (f1 clob);
drop view if exists to_clob_view;
insert into test2 values (3);
create view to_clob_view as select * from test2 where f1>to_clob(2);
select * from to_clob_view;
drop view if exists to_clob_view;
drop table if exists test2;