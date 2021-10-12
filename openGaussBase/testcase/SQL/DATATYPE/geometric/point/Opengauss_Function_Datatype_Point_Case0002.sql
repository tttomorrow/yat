-- @testpoint: point类型，使用(x,y)方式插入负数坐标值

drop table if exists test_point02;
create table test_point02 (name point);
insert into test_point02 values (point '(-1,-1)');
insert into test_point02 values (point '(-1.23,-1.056)');
insert into test_point02 values (point '(-12.11,-0.361)');
select * from test_point02;
drop table test_point02;