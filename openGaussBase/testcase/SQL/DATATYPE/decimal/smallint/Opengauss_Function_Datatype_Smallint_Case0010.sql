-- @testpoint: 插入字符串类型，合理报错

drop table if exists smallint10;
create table smallint10 (name smallint);
insert into smallint10 values ('123abc');
insert into smallint10 values ('aabbcc');
insert into smallint10 values ('abc456');
drop table smallint10;