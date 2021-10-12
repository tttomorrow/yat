-- @testpoint: path类型，使用[(x1,y1),...,(xn,yn)]方式插入正数坐标值

drop table if exists test_path02;
create table test_path02 (name path);
insert into test_path02 values (path'[(-1,-1),(-2,-2),(-3,-3)]');
insert into test_path02 values (path'[(-1.2,-1.3),(-2.2,-2.3),(-3.301,-3.226)]');
insert into test_path02 values (path'[(-1,-1),(-2,-2),(-3,-3),(-4,-4)]');
insert into test_path02 values (path'[(-1.02,-1.32),(-2.52,-2.002),(-3.23,-3.33),(-4.12,-4.023)]');
select * from test_path02;
drop table test_path02;