-- @testpoint: lseg类型，使用[(x1,y1),(x2,y2)]方式插入较大坐标值

drop table if exists test_lseg04;
create table test_lseg04 (name lseg);
insert into test_lseg04 values (lseg '[(99999999999999999999999999999,99999999999999999999999999999999),(99999999999999999999999999999,99999999999999999999999999999999)]');
insert into test_lseg04 values (lseg '[(0,0),(99999999999999999999999999999,99999999999999999999999999999999)]');
select * from test_lseg04;
drop table test_lseg04;