-- @testpoint: 插入特殊字符
-- @modify at: 2020-11-05


DROP TABLE IF EXISTS type_char13;
CREATE TABLE type_char13 (stringv char(20));
insert into type_char13 values ('$@#%……&*（）');
select * from type_char13;
drop table type_char13;
