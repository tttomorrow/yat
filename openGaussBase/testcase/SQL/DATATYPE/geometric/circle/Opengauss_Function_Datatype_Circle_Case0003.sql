-- @testpoint: circle类型，使用<(x,y),r>方式插入值0坐标值(圆心)

drop table if exists test_circle03;
create table test_circle03 (name circle);
insert into test_circle03 values (circle '<(0,0),2>');
select * from test_circle03;
drop table test_circle03;