-- @testpoint: 插入字符串类型数值

drop table if exists smallint04;
create table smallint04 (name smallint);
insert into smallint04 values ('1236');
insert into smallint04 values ('11111');
insert into smallint04 values ('-1236');
insert into smallint04 values ('-1');
insert into smallint04 values ('-2');
insert into smallint04 values ('-3');
select * from smallint04;
drop table smallint04;