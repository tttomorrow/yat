-- @testpoint: 插入指数形式值

drop table if exists integer07;
create table integer07 (name integer);
insert into integer07 values (exp(3));
insert into integer07 values (exp(1.23));
insert into integer07 values (exp(-5));
insert into integer07 values (exp(-1.5));
select * from integer07;
drop table integer07;