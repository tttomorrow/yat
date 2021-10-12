-- @testpoint: path类型，使用[(x1,y1),...,(xn,yn)]方式插入空坐标值，合理报错

drop table if exists test_path05;
create table test_path05 (name path);
insert into test_path05 values (path '[(null,null),(null,null),(null,null)]');
insert into test_path05 values (path '[('',''),('',''),('','')]');
drop table test_path05;