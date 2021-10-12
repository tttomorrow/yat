-- @testpoint: box类型，使用(x1,y1),(x2,y2)方式插入0点坐标

drop table if exists test_box03;
create table test_box03 (name box);
insert into test_box03 values (box '(0,0),(0,0)');
select * from test_box03;
drop table test_box03;