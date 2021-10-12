-- @testpoint: 输入日期上限，如：9999-12-31

drop table if exists test_date01;
create table test_date01 (name date);
insert into test_date01 values ('9999-12-31');
select * from test_date01;
drop table test_date01;