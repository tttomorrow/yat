-- @testpoint: 插入字符串形式数值

drop table if exists real_04;
create table real_04 (name real);
insert into real_04 values ('14165132.99999');
insert into real_04 values ('999999');
insert into real_04 values ('-14165132.999999');
insert into real_04 values ('-999999');
select * from real_04;
drop table real_04;
