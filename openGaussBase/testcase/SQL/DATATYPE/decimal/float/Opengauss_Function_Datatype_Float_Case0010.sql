-- @testpoint: 插入bool类型,合理报错

drop table if exists float10;
create table float10 (name float);
insert into float10 values (true);
insert into float10 values (false);
drop table float10;