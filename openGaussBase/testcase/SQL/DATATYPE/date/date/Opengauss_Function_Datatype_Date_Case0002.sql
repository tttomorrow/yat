-- @testpoint: 输入超出日期上下限，合理报错

drop table if exists test_date02;
create table test_date02 (name date);
insert into test_date02 values ('0000-00-00');
insert into test_date02 values ('9999-12-32');
drop table test_date02;