-- @testpoint: path类型，使用[(x1,y1),...,(xn,yn)]方式插入0坐标值

drop table if exists test_path03;
create table test_path03 (name path);
insert into test_path03 values (path'[(0,0),(0,0),(0,0)]');
select * from test_path03;
drop table test_path03;