-- @testpoint: lseg类型，使用[(x1,y1),(x2,y2)]方式插入正数坐标值

drop table if exists test_lseg01;
create table test_lseg01 (name lseg);
insert into test_lseg01 values (lseg '[(1,1),(2,2)]');
insert into test_lseg01 values (lseg '[(1.2,1.3),(2.3,2.4)]');
insert into test_lseg01 values (lseg '[(10,10.23),(22,2.023)]');
select * from test_lseg01;
drop table test_lseg01;