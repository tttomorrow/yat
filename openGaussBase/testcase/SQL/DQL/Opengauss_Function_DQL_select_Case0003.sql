-- @testpoint: DQL语法，覆盖英文

drop table if exists test_clob;
create table test_clob(id int,c_clob clob);
insert into test_clob values(1,'qwertyuioplmnb');
insert into test_clob values(2,'asdfghjkl');
insert into test_clob values(3,'zxcvb');
insert into test_clob values(4,'hello');

select * from test_clob where c_clob='qwertyuioplmnb';
select * from test_clob where c_clob='asdfghjkl';
select * from test_clob where c_clob='zxcvb';
select * from test_clob where c_clob='hello';

drop table test_clob;

