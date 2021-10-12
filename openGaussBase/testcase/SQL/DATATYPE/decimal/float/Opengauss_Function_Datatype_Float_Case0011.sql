-- @testpoint: 插入指数形式值

drop table if exists float11;
create table float11 (name float);
insert into float11 values (exp(33));
insert into float11 values (exp(12.33));
insert into float11 values (exp(-33));
insert into float11 values (exp(-12.33));
select * from float11;
drop table float11;