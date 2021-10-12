-- @testpoint: 插入超出左边界范围值，合理报错

drop table if exists float06;
create table float06 (name float);
insert into float06 values (1E-325);
drop table float06;
