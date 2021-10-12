-- @testpoint: round函数函数嵌套的测试
drop table if exists tb;
create table tb (dp1 double precision, nem numeric);
insert into tb values (99999.2,10000.134);
insert into tb values (9.2, 9.56);
select round(round(dp1)),round(round(nem)) from tb order by 2;
drop table tb;