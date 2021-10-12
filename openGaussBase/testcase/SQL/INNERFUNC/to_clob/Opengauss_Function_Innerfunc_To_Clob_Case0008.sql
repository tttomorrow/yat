-- @testpoint: 是否支持where条件查询

drop table if exists test2;
create table test2 (f2 clob);
insert into test2 values(11);
select * from test2 where f2=to_clob(11);
drop table if exists test2;