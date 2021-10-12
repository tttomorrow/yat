-- @testpoint: path类型，使用[(x1,y1),...,(xn,yn)]方式插入较大坐标值

drop table if exists test_path04;
create table test_path04 (name path);
select * from test_path04;
drop table test_path04;