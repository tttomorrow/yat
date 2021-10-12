-- @testpoint: box类型，使用(x1,y1),(x2,y2)方式插入正数坐标值

drop table if exists test_box01;
create table test_box01 (name box);
insert into test_box01 values (box '(1,1),(2,2)');
insert into test_box01 values (box '(1.2,1.3),(2.1,2.2)');
insert into test_box01 values (box '(12,1.123),(26,2.789)');
select * from test_box01;
drop table test_box01;