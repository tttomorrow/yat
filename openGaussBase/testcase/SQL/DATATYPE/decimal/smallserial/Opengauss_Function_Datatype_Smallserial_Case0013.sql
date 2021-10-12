-- @testpoint: 插入0值

drop table if exists smallserial_13;
create table smallserial_13 (name smallserial);
insert into smallserial_13 values (0);
insert into smallserial_13 values (0);
insert into smallserial_13 values (0);
select * from smallserial_13;
drop table smallserial_13;