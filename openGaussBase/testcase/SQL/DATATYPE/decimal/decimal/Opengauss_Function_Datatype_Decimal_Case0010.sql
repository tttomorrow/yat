-- @testpoint: 插入bool类型

drop table if exists decimal_10;
create table decimal_10 (name decimal);
insert into decimal_10 values (true);
insert into decimal_10 values (false);
select * from decimal_10;
drop table decimal_10;