-- @testpoint: 插入bool类型

drop table if exists numeric_10;
create table numeric_10 (name numeric);
insert into numeric_10 values (false);
insert into numeric_10 values (true);
drop table numeric_10;