-- @testpoint: point类型，使用(x,y)方式插入正数坐标值

drop table if exists test_point01;
create table test_point01 (name point);
insert into test_point01 values (point '(1,1)');
insert into test_point01 values (point '(1.25,1.36)');
insert into test_point01 values (point '(1000,0.1231)');
select * from test_point01;
drop table test_point01;