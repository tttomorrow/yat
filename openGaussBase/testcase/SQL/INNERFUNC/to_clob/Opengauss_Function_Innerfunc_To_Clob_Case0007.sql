-- @testpoint: to_clob函数作为concat（）函数入参

drop table if exists test2;
create table test2 (f2 clob);
insert into test2 values(concat(to_clob('1111'),(2222),('3333')));
select * from test2;
drop table if exists test2;