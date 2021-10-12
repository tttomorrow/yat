-- @testpoint: 插入bool类型

drop table if exists smallserial_10;
create table smallserial_10 (name smallserial);
insert into smallserial_10 values (false);
insert into smallserial_10 values (true);
select * from smallserial_10;
drop table smallserial_10;