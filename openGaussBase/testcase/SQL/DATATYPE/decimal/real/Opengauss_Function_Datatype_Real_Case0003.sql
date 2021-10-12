-- @testpoint: 插入浮点数

drop table if exists real_03;
create table real_03 (name real);
insert into real_03 values (12122.12);
insert into real_03 values (0.00001);
insert into real_03 values (-12122.23);
insert into real_03 values (-0.00001);
select * from real_03;
drop table real_03;
