-- @testpoint: 插入超出左边界范围外值，隐式转换为smallint

drop table if exists smallserial_06;
create table smallserial_06 (name smallserial);
insert into smallserial_06 values (0);
select * from smallserial_06;
drop table smallserial_06;