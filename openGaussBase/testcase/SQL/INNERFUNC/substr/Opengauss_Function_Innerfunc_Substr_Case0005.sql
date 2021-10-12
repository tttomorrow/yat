-- @testpoint: substr函数作为where条件
drop table if exists test;
create table test(id int, name text);
insert into test values(1,'university students');
insert into test values(2,'university labary');
insert into test values(3,'university playground');
insert into test values(4,'university classroom');
insert into test values(5,'kindergarten child');
select id,name from test where substr(name,1,10) != 'university';
drop table test;