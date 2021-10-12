-- @testpoint: polygon类型，使用(x1,y1),...,(xn,yn)方式插入空坐标值,合理报错

drop table if exists test_polygon05;
create table test_polygon05 (name polygon);
insert into test_polygon05 values (polygon '(null,null),(null,null),(null,null)');
insert into test_polygon05 values (polygon '('',''),('',''),('','')');
drop table test_polygon05;