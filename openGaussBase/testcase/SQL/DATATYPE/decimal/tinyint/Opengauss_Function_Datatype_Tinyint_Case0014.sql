-- @testpoint: 插入空值

drop table if exists tinyint14;
create table tinyint14 (id int,name tinyint);
insert into tinyint14 values (1,null);
insert into tinyint14 values (2,'');
select * from tinyint14;
drop table tinyint14;