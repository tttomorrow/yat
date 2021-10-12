-- @testpoint: 插入空值
-- @modify at: 2020-11-05

DROP TABLE IF EXISTS type_boolean03;
CREATE TABLE type_boolean03 (datev boolean);
insert into type_boolean03 values (null);
insert into type_boolean03 values ('');
select * from type_boolean03;
drop table type_boolean03;