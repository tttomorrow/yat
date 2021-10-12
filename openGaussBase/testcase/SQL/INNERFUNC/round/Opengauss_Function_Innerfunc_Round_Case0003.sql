-- @testpoint: round函数入参为无精度数值类型
drop table if exists tb;
create table tb (num int,dp1 double precision,nem numeric);
insert into tb (nem) values(43.4);
insert into tb (nem) values(43.5);
select round(nem) as result from tb where nem in (43.4,43.5) order by 1;
drop table tb;