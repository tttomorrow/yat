-- @testpoint: EXTRACT函数判断传入的TIMESTAMP类型是星期几 
drop table if exists test_date01;
create table test_date01 (clo1 TIMESTAMP);
insert into test_date01 values ('2020-08-16 00:00:00');
insert into test_date01 values ('2020-08-17');
insert into test_date01 values ('1998-01-01');
insert into test_date01 values ('1830-01-01 23:00:00 pst');
insert into test_date01 values ('2020-08-22 00:00:00+8');
select EXTRACT(dow FROM clo1) from test_date01;
SELECT EXTRACT(dow FROM TIMESTAMP '0001-01-01 00:00:00');
SELECT EXTRACT(dow FROM TIMESTAMP '0101-01-01 00:00:00');
SELECT EXTRACT(dow FROM TIMESTAMP '0218-01-01 pst');
SELECT EXTRACT(dow FROM TIMESTAMP '1998-01-01');
SELECT EXTRACT(dow FROM TIMESTAMP '1830-01-01 23:00:00 pst');
SELECT EXTRACT(dow FROM TIMESTAMP '9999-12-31 00:00:00+8');
drop table if exists test_date01;