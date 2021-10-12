-- @testpoint: 插入正常值，将name数据类型转换至boolean、date，合理报错
-- @modified at: 2020-11-13

drop table if exists name_04;
CREATE TABLE name_04 (id name);
insert into name_04 values (11.11);
alter table name_04 alter column id type boolean;
alter table name_04 alter column id type date;
select * from name_04;
drop table name_04;