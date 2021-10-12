-- @testpoint: polygon类型，使用(x1,y1),...,(xn,yn)方式插入0坐标值

drop table if exists test_polygon03;
create table test_polygon03 (name polygon);
insert into test_polygon03 values (polygon '(0,0),(0,0),(0,0)');
select * from test_polygon03;
drop table test_polygon03;