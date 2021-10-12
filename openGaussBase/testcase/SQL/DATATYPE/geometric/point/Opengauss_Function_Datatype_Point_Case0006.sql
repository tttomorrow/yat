-- @testpoint: point类型，插入无效坐标值，合理报错

drop table if exists test_point06;
create table test_point06 (name point);
insert into test_point06 values (point'(a,b)');
insert into test_point06 values (point'(~,~)');
insert into test_point06 values (point'(@,@)');
insert into test_point06 values (point'(#,#)');
insert into test_point06 values (point'(,)');
drop table test_point06;