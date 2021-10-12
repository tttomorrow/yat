-- @testpoint: path类型，插入无效坐标值，合理报错

drop table if exists test_path06;
create table test_path06 (name path);
insert into test_path06 values (path '(a,b),(a,b),(a,b)');
insert into test_path06 values (path '(~,~),(~,~),(~,~)');
insert into test_path06 values (path '(@,@),(@,@),(@,@)');
insert into test_path06 values (path '(#,#),(#,#),(#,#)');
insert into test_path06 values (path '(,),(,),(,)');
drop table test_path06;