-- @testpoint: 插入字符串形式数值

drop table if exists decimal_04;
create table decimal_04 (name decimal);
insert into decimal_04 values ('14165132.99999');
insert into decimal_04 values ('9999999');
insert into decimal_04 values ('-14165132.999999');
insert into decimal_04 values ('-9999999');
select * from decimal_04;
drop table decimal_04;
