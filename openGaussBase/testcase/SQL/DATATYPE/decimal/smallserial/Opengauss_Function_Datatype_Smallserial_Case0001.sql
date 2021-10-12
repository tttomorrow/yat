-- @testpoint: 插入正整数

drop table if exists smallserial_01;
create table smallserial_01 (name smallserial);
insert into smallserial_01 values (120);
insert into smallserial_01 values (11111);
insert into smallserial_01 values (1);
insert into smallserial_01 values (2);
insert into smallserial_01 values (3);
select * from smallserial_01;
drop table smallserial_01;