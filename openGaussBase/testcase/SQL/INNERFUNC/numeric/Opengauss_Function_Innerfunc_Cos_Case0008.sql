-- @testpoint: cos函数与when联合使用
drop table if exists tb1;
create table tb1(flag varchar, col_cos double precision);
insert into tb1 values('no1', 2*pi());
insert into tb1 values('no2', -2*pi());
insert into tb1 values('no3', 4*pi());
insert into tb1 values('no4', 337);
insert into tb1 values('no5', -99.99);
insert into tb1 values('no6', -598*pi());
select * from tb1 where cos(col_cos) = 1;
drop table tb1;