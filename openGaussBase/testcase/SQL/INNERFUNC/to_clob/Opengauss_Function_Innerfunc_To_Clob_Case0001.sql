-- @testpoint:  varchar2类型转换clob类型

drop table if exists test2;
create table test2 (d varchar2);
insert into test2 values('nihao');
select to_clob(d) from test2;
drop table if exists test2;