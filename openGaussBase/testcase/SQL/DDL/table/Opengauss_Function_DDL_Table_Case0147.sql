-- @testpoint: 创建列类型是网络地址类型的表
drop table if exists table_2;
create table table_2(a cidr,b inet,c macaddr);
insert into table_2 (a)  values('192.168.100.128/25');
insert into table_2 values('192.168.0.0/24','::ffff:1.2.3/120','0800.2b01.0203');
select * from table_2;
drop table if exists table_2;