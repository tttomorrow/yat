-- @testpoint: 插入指数形式值

drop table if exists real_07;
create table real_07 (name real);
insert into real_07 values (exp(33));
insert into real_07 values (exp(1.23));
insert into real_07 values (exp(-15));
insert into real_07 values (exp(-1.5));
select * from real_07;
drop table real_07;