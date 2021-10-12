-- @testpoint: to_clob函数与order by联合使用

drop table if exists test2;
create table test2 (f2 clob);
insert into test2 values(5);
insert into test2 values(6);
insert into test2 values(7);
insert into test2 values(8);
select * from test2 where f2>to_clob(5) order by to_char(f2);
drop table if exists test2;