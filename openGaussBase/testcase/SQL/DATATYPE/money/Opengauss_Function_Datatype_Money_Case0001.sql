-- @testpoint: 插入正整数

drop table if exists type_money01;
create table type_money01 (mon money);
insert into type_money01 values (132);
insert into type_money01 values (1);
insert into type_money01 values (2);
insert into type_money01 values (3);
select * from type_money01;
drop table type_money01;