-- @testpoint: 超出上下限，合理报错

drop table if exists test_timestamp16;
create table test_timestamp16 (name timestamp);
insert into test_timestamp16 values (TIMESTAMP '0000-00-00 00:00:00.000000','yyyy-mm-dd hh24:mi:ss.ff');
insert into test_timestamp16 values (TIMESTAMP '9999-12-31 23:59:59.999999','yyyy-mm-dd hh24:mi:ss.ff');
select * from test_timestamp16;
drop table if exists test_timestamp16;