-- @testpoint: 插入0值

drop table if exists numeric_13;
create table numeric_13 (name numeric);
insert into numeric_13 values (0);
insert into numeric_13 values (0);
insert into numeric_13 values (0);
select * from numeric_13;
drop table numeric_13;