-- @testpoint: 插入空值

drop table if exists bigint15;
create table bigint15 (id int,name bigint);
insert into bigint15 values (1,null);
insert into bigint15 values (2,'');
select * from bigint15;
drop table bigint15;