-- @testpoint: 插入空值

drop table if exists int13;
create table int13 (id dec,name int);
insert into int13 values (1,'');
insert into int13 values (2,null);
select * from int13;
drop table int13;