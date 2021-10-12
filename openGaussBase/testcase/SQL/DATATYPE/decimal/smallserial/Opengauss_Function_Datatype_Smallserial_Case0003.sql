-- @testpoint: 插入浮点数

drop table if exists smallserial_03;
create table smallserial_03 (name smallserial);
insert into smallserial_03 values (12122.12);
insert into smallserial_03 values (0.000001);
insert into smallserial_03 values (-12122.23);
insert into smallserial_03 values (-0.000001);
select * from smallserial_03;
drop table smallserial_03;
