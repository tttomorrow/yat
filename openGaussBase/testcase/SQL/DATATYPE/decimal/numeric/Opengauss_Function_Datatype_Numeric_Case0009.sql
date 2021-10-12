-- @testpoint: 插入字符串类型数值

drop table if exists numeric_09;
create table numeric_09 (name numeric);
insert into numeric_09 values ('12354563');
insert into numeric_09 values ('123.456');
insert into numeric_09 values ('-12354563');
insert into numeric_09 values ('-123.456');
select * from numeric_09;
drop table numeric_09;