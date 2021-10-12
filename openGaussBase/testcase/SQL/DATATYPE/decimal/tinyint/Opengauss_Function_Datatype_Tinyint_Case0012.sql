-- @testpoint: 插入指数形式值

drop table if exists tinyint12;
create table tinyint12 (name tinyint);
insert into tinyint12 values (exp(3));
insert into tinyint12 values (exp(1.5));
insert into tinyint12 values (exp(-5));
insert into tinyint12 values (exp(-1.5));
select * from tinyint12;
drop table tinyint12;