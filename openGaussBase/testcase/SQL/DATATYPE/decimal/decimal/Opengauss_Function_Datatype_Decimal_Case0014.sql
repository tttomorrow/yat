-- @testpoint: 插入空值

drop table if exists decimal_14;
create table decimal_14 (id int,name decimal);
insert into decimal_14 values (1,null);
insert into decimal_14 values (2,'');
select * from decimal_14;
drop table decimal_14;