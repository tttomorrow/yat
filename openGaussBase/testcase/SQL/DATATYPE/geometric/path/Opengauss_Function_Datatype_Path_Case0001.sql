-- @testpoint: path类型，使用[(x1,y1),...,(xn,yn)]方式插入正数坐标值

drop table if exists test_path01;
create table test_path01 (name path);
insert into test_path01 values (path '[(1,1),(2,2),(3,3)]');
insert into test_path01 values (path '[(1.2,1.5),(2.23,2.55),(3.21,3.00)]');
insert into test_path01 values (path '[(1,1),(2,2),(3,3),(4,4)]');
insert into test_path01 values (path '[(1.02,1.302),(2.23,2.56),(3.23,3.222),(4.456,4.333)]');
select * from test_path01;
drop table test_path01;