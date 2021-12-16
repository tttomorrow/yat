-- @testpoint: box类型，使用(x1,y1),(x2,y2)方式插入较大坐标值

drop table if exists test_box04;
create table test_box04 (name box);
insert into test_box04 values (box '(99999999999999999999999999999,99999999999999999999999999999999),(99999999999999999999999999999,99999999999999999999999999999999)');
select * from test_box04;
drop table test_box04;