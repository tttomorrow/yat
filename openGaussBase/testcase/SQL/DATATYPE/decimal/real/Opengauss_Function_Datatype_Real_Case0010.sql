-- @testpoint: 插入空值

drop table if exists real_10;
create table real_10 (id int,name real);
insert into real_10 values (1,null);
insert into real_10 values (2,'');
select * from real_10;
drop table real_10;