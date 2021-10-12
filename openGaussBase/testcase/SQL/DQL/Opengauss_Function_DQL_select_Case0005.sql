-- @testpoint: DQL语法，覆盖长字符串

drop table if exists test_clob;
create table test_clob(id int,c_clob clob);
insert into test_clob values(1,lpad('hello',8888,'hello'));
insert into test_clob values(1,lpad('hello',88888,'hello'));
insert into test_clob values(1,lpad('hello',888888,'hello'));

select char_length(c_clob) from test_clob where id=1;

drop table test_clob;