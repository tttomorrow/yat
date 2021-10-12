-- @testpoint: circle类型，使用<(x,y),r>方式插入无效坐标值(圆心)，合理报错

drop table if exists test_circle06;
create table test_circle06 (name circle);
insert into test_circle06 values (circle '<(a,b),2>');
insert into test_circle06 values (circle '<(~,~),2>');
insert into test_circle06 values (circle '<(@,@),2>');
insert into test_circle06 values (circle '<(#,#),2>');
insert into test_circle06 values (circle '<(,),2>');
drop table test_circle06;