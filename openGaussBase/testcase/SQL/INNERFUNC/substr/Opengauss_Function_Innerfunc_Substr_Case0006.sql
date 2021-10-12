-- @testpoint: substr函数与having联合使用
drop table if exists test;
create table test(id int, name text);
insert into test values(122,'university students');
insert into test values(21,'university labary');
insert into test values(35,'university playground');
insert into test values(411,'university classroom');
insert into test values(5,'kindergarten child');
select name from test group by name having substr(name,1,10) = 'university';
drop table test;