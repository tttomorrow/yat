-- @testpoint: lseg类型，使用[(x1,y1),(x2,y2)]方式插入无效坐标值，合理报错

drop table if exists test_lseg06;
create table test_lseg06 (name lseg);
insert into test_lseg06 values (lseg '[(a,b),(a,b)]');
insert into test_lseg06 values (lseg '[(~,~),(~,~)]');
insert into test_lseg06 values (lseg '[(@,@),(@,@)]');
insert into test_lseg06 values (lseg '[(#,#),(#,#)]');
insert into test_lseg06 values (lseg '[(,),(,)]');
drop table test_lseg06;