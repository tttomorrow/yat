-- @testpoint: 插入正整数

drop table if exists int10;
create table int10 (name int);
insert into int10 values (1223340);
insert into int10 values (999999999);
insert into int10 values (1);
insert into int10 values (2);
insert into int10 values (3);
select * from int10;
drop table int10;