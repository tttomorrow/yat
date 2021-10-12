-- @testpoint: EXTRACT函数从TIMESTAMP类型中获取day
drop table if exists test_date01;
create table test_date01 (clo1 TIMESTAMP);
insert into test_date01 values ('2001-02-16 20:38:40');
SELECT EXTRACT(DAY FROM TIMESTAMP '2001-02-16 20:38:40');
drop table if exists test_date01;