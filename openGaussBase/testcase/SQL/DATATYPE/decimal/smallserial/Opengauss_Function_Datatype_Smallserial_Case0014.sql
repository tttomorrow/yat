-- @testpoint: 插入空值,合理报错

drop table if exists smallserial_14;
create table smallserial_14 (id int,name smallserial);
insert into smallserial_14 values (1,null);
insert into smallserial_14 values (2,'');
drop table smallserial_14;