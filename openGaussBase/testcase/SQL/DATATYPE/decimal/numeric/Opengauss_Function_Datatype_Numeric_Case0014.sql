-- @testpoint: 插入空值

drop table if exists numeric_14;
create table numeric_14 (id int,name numeric);
insert into numeric_14 values (1,null);
insert into numeric_14 values (2,'');
select * from numeric_14;
drop table numeric_14;