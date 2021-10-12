-- @testpoint: point类型，使用(x,y)方式插入空坐标值，合理报错

drop table if exists test_point05;
create table test_point05 (name point);
insert into test_point05 values (point '(null,null)');
drop table test_point05;
