-- @testpoint: 插入特殊字符，合理报错

drop table if exists smallint05;
create table smallint05 (name smallint);
insert into smallint05 values (@);
insert into smallint05 values ('#');
drop table smallint05;