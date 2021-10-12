-- @testpoint: 插入浮点数

drop table if exists binary_double03;
create table binary_double03 (name binary_double);
insert into binary_double03 values (12122.3340);
insert into binary_double03 values (0.000002);
insert into binary_double03 values (-3333.2222);
insert into binary_double03 values (-0.003);
select * from binary_double03;
drop table binary_double03;
