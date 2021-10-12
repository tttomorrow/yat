-- @testpoint: polygon类型，插入无效坐标值，合理报错

drop table if exists test_polygon06;
create table test_polygon06 (name polygon);
insert into test_polygon06 values (polygon'(a,b),(a,b),(a,b)');
insert into test_polygon06 values (polygon'(~,~),(~,~),(~,~)');
insert into test_polygon06 values (polygon'(@,@),(@,@),(@,@)');
insert into test_polygon06 values (polygon'(#,#),(#,#),(#,#)');
insert into test_polygon06 values (polygon'(,),(,),(,)');
drop table test_polygon06;