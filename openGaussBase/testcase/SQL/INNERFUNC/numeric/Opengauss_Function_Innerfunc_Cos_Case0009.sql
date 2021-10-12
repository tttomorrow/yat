-- @testpoint: cos函数入参为正负无穷大,合理报错
drop table if exists tb1;
create table tb1(col_cos double precision);
insert into tb1 values('infinity');
insert into tb1 values('-infinity');
select cos(col_cos) as result from tb1;
drop table tb1;