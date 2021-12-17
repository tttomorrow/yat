-- @testpoint: polygon类型，使用(x1,y1),...,(xn,yn)方式插入较大坐标值

drop table if exists test_polygon04;
create table test_polygon04 (name polygon);
insert into test_polygon04 values (polygon'(99999999999999999999999999999,99999999999999999999999999999999),(99999999999999999999999999999,99999999999999999999999999999999),(99999999999999999999999999999,99999999999999999999999999999999)');
select * from test_polygon04;
drop table test_polygon04;