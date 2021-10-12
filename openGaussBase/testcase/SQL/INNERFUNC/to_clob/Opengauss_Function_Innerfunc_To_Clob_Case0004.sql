-- @testpoint: char类型转换clob类型

drop table if exists test2;
create table test2 (d char(10));
insert into test2 values ('hello111');
select to_clob(d) from test2;
drop table if exists test2;