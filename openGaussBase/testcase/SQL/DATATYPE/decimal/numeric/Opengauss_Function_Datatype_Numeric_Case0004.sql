-- @testpoint: 插入字符串形式数值

drop table if exists numeric_04;
create table numeric_04 (name numeric);
insert into numeric_04 values ('14165132.99999');
insert into numeric_04 values ('-14165132.999999');
insert into numeric_04 values ('999456');
insert into numeric_04 values ('-999456');
select * from numeric_04;
drop table numeric_04;
