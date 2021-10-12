-- @testpoint: 插入0值

drop table if exists decimal_13;
create table decimal_13 (name decimal);
insert into decimal_13 values (0);
insert into decimal_13 values (0);
insert into decimal_13 values (0);
select * from decimal_13;
drop table decimal_13;