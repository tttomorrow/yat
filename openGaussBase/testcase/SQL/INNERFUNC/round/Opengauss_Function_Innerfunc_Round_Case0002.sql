-- @testpoint: round函数入参为双精度类型
drop table if exists tb;
create table tb (num int,dp1 double precision,nem numeric);
insert into tb (dp1) values(round(cast(43.4 as double precision)));
insert into tb (dp1) values(round(cast(43.5 as double precision)));
select dp1 as result from tb order by 1;
drop table if exists tb;