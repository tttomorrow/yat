-- @testpoint: lseg类型，使用[(x1,y1),(x2,y2)]方式插入0坐标值

drop table if exists test_lseg03;
create table test_lseg03 (name lseg);
insert into test_lseg03 values (lseg '[(0,0),(0,0)]');
select * from test_lseg03;
drop table test_lseg03;