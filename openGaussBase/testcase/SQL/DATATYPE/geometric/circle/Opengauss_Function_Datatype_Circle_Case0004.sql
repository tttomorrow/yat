-- @testpoint: circle类型，使用<(x,y),r>方式插入较大坐标值(圆心)

drop table if exists test_circle04;
create table test_circle04 (name circle);
select * from test_circle04;
drop table test_circle04;