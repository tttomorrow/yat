-- @testpoint: 插入指数形式值

drop table if exists numeric_11;
create table numeric_11 (name numeric);
insert into numeric_11 values (exp(33));
insert into numeric_11 values (exp(1.23));
insert into numeric_11 values (exp(-15));
insert into numeric_11 values (exp(-1.56));
select * from numeric_11;
drop table numeric_11;