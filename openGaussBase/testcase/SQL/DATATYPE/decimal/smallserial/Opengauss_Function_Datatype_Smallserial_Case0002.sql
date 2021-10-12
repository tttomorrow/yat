-- @testpoint: 插入负整数

drop table if exists smallserial_02;
create table smallserial_02 (name smallserial);
insert into smallserial_02 values (-121);
insert into smallserial_02 values (-11111);
insert into smallserial_02 values (-1);
insert into smallserial_02 values (-2);
insert into smallserial_02 values (-3);
select * from smallserial_02;
drop table smallserial_02;
