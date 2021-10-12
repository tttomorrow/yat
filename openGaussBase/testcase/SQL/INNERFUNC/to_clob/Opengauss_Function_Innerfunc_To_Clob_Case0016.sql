-- @testpoint: raw类型转换为clob类型

drop table if exists test2;
create table test2 (d raw);
insert into test2 values('ABCDEF');
select to_clob(d) from test2;
drop table if exists test2;