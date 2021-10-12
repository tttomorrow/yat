-- @testpoint: 不指定精度，插入浮点数

drop table if exists numeric_03;
create table numeric_03 (name numeric);
insert into numeric_03 values (12122.12);
insert into numeric_03 values (-12122.23);
insert into numeric_03 values (0.000001);
insert into numeric_03 values (-0.000001);
select * from numeric_03;
drop table numeric_03;
