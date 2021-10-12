-- @testpoint: to_clob和‘||’结合

drop table if exists test2;
create table test2 (f2 clob);
insert into test2 values(to_clob('1111111??????????')||to_clob('444aaaaaaaa44444')||to_clob('qqq55555'));
select * from test2;
drop table if exists test2;