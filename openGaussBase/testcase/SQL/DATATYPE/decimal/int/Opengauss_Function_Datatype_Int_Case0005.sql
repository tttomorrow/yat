-- @testpoint: 插入字符串类型数值

drop table if exists int05;
create table int05 (name int);
insert into int05 values ('123456');
insert into int05 values ('999999');
insert into int05 values ('-123456');
insert into int05 values ('-556677');
select * from int05;
drop table int05;