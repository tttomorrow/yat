-- @testpoint: 插入非法空值,合理报错

drop table if exists dec_05;
CREATE  TABLE dec_05 (id1 int,id2 DEC(4,2));
insert into dec_05 values (1,' ');
drop table dec_05;