-- @testpoint: point类型，使用(x,y)方式插入较大坐标值

drop table if exists test_point04;
create table test_point04 (name point);
insert into test_point04 values (point'(99999999999999999999999999999,99999999999999999999999999999999)');
select * from test_point04;
drop table test_point04;