-- @testpoint: 插入左边界范围值

drop table if exists smallserial_05;
create table smallserial_05 (name smallserial);
insert into smallserial_05 values (1);
select * from smallserial_05;
drop table smallserial_05;