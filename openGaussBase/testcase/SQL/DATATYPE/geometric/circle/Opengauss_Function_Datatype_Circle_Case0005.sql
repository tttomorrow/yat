-- @testpoint: circle类型，使用<(x,y),r>方式插入空坐标值(圆心)，合理报错

drop table if exists test_circle05;
create table test_circle05 (name circle);
insert into test_circle05 values (circle '<(null,null),2>');
drop table test_circle05;