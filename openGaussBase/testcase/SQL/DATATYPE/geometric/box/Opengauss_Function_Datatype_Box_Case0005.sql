-- @testpoint: box类型，使用(x1,y1),(x2,y2)方式插入空值，合理报错

drop table if exists test_box05;
create table test_box05 (name box);
insert into test_box05 values (box '(null,null),(null,null)');
insert into test_box05 values (box '('',''),('','')');
select * from test_box05;
drop table test_box05;