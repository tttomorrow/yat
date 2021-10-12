-- @testpoint: 插入字符串类型，合理报错

drop table if exists bigint10;
create table bigint10 (name bigint);
insert into bigint10 values ('123abc');
insert into bigint10 values ('abcde');
insert into bigint10 values ('abc456');
drop table bigint10;