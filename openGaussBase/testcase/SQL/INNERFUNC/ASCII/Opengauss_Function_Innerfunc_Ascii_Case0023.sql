-- @testpoint: 与distinct联用
drop table if exists test;
create table test(name text);
insert into test values('a'),('j'),('Hi'),('Hello'),('Hello'),('#');
select distinct chr(ascii(name)) from test order by chr(ascii(name));
drop table if exists test;