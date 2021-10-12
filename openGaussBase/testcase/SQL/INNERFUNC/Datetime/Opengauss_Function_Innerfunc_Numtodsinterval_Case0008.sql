--  @testpoint: numtodsinterval interval_unit为 ’DAY‘兼容格式输出多位小数

drop table if exists test_date01;
create table test_date01 (clo1 date);
insert into test_date01 values ('2001-02-16');
SET intervalstyle = a;
drop table if exists test_date01;