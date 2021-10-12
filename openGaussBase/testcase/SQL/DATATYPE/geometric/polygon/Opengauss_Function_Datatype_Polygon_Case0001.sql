-- @testpoint: polygon类型，使用(x1,y1),...,(xn,yn)方式插入正数坐标值

drop table if exists test_polygon01;
create table test_polygon01 (name polygon);
insert into test_polygon01 values (polygon '(1,1),(2,2),(3,3)');
insert into test_polygon01 values (polygon '(1.01,1.23),(2.12,2.333),(3.33,3.45)');
insert into test_polygon01 values (polygon '(1,1),(2,2),(3,3),(4,4)');
insert into test_polygon01 values (polygon '(1.12,1.023),(2.556,2.78),(3.02,3.22),(4.45,4.23)');
select * from test_polygon01;
drop table test_polygon01;