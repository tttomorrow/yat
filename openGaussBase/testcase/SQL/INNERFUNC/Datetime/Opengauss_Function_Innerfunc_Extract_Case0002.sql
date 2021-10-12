-- @testpoint: EXTRACT函数从TIMESTAMP类型中获取最大世纪
drop table if exists test_date01;
create table test_date01 (clo1 TIMESTAMP);
insert into test_date01 values ('9999-12-31 00:00:00');
select EXTRACT(CENTURY FROM clo1) from test_date01;
SELECT EXTRACT(CENTURY FROM TIMESTAMP '9999-12-31 00:00:00');
drop table if exists test_date01;