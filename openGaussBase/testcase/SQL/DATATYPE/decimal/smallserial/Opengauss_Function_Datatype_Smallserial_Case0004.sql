-- @testpoint: 插入字符串形式数值

drop table if exists smallserial_04;
create table smallserial_04 (name smallserial);
insert into smallserial_04 values ('9999');
insert into smallserial_04 values ('1');
insert into smallserial_04 values ('2');
insert into smallserial_04 values ('-9999');
insert into smallserial_04 values ('-1');
insert into smallserial_04 values ('-2');
select * from smallserial_04;
drop table smallserial_04;
