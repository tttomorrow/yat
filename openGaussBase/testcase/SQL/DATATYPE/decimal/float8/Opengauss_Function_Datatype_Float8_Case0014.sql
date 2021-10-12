-- @testpoint: 插入空值

drop table if exists float8_14;
create table float8_14 (id int,name float8);
insert into float8_14 values (1,null);
insert into float8_14 values (2,'');
select * from float8_14;
drop table if exists float8_14;