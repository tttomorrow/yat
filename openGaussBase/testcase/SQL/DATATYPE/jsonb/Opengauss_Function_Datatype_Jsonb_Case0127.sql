-- @testpoint: 修改为其他数据类型为jsonb,不支持直接转化，合理报错

--创建数据类型为其他数据类型的表,修改表的数据类型为jsonb
--char-->jsonb
drop table if exists tab127;
create table tab127(id int,name varchar,address char(50),number text);
insert into tab127 values(023,'Jack','{"age":20,"city":"xiamen"}',158237664);
alter table tab127 modify address jsonb;

--varchar-->jsonb
alter table tab127 modify name jsonb;

--text-->jsonb
alter table tab127 modify number jsonb;

--int-->jsonb
alter table tab127 modify id jsonb;
drop table if exists tab127;