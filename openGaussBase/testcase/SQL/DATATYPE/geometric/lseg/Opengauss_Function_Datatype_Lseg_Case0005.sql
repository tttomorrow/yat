-- @testpoint: lseg类型，使用[(x1,y1),(x2,y2)]方式插入空坐标值，合理报错

drop table if exists test_lseg05;
create table test_lseg05 (name lseg);
insert into test_lseg05 values (lseg '[(null,null),(null,null)]');
insert into test_lseg05 values (lseg '[('',''),('','')]');
drop table test_lseg05;