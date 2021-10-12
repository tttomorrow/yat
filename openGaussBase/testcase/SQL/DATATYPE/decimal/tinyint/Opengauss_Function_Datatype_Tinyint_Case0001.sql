-- @testpoint: 插入正整数

drop table if exists tinyint01;
create table tinyint01 (name tinyint);
insert into tinyint01 values (120);
insert into tinyint01 values (1);
insert into tinyint01 values (2);
insert into tinyint01 values (3);
insert into tinyint01 values (5);
select * from tinyint01;
drop table tinyint01;