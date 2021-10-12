-- @testpoint: 插入default自定义值

drop table if exists smallserial_15;
create table smallserial_15 (name smallserial);
insert into smallserial_15 values (default);
insert into smallserial_15 values (default);
insert into smallserial_15 values (default);
select * from smallserial_15;
drop table smallserial_15;