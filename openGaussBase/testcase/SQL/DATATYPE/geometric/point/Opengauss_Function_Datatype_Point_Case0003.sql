-- @testpoint: point类型，使用(x,y)方式插入0坐标值

drop table if exists test_point03;
create table test_point03 (name point);
insert into test_point03 values (point '(0,0)');
select * from test_point03;
drop table test_point03;