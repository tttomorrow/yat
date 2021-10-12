-- @testpoint:  bigint类型转换clob类型

drop table if exists test2;
create table test2 (d bigint);
insert into test2 values(12345);
select to_clob(d) from test2;
drop table if exists test2;