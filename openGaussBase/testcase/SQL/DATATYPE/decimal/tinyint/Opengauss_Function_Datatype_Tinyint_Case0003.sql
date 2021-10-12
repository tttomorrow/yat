-- @testpoint: 插入浮点数

drop table if exists tinyint03;
create table tinyint03 (name tinyint);
insert into tinyint03 values (122.3340);
insert into tinyint03 values (0.000001);
insert into tinyint03 values (99.99);
select * from tinyint03;
drop table tinyint03;
