-- @testpoint: box类型，插入无效坐标值，合理报错

drop table if exists test_box06;
create table test_box06 (name box);
insert into test_box06 values (box'(a,b),(a,b)');
insert into test_box06 values (box'(~,~),(~,~)');
insert into test_box06 values (box'(@,@),(@,@)');
insert into test_box06 values (box'(#,#),(#,#)');
insert into test_box06 values (box'(,),(,)');
drop table test_box06;