-- @testpoint: 插入空值
-- @modified at: 2020-11-13

drop table if exists name_05;
CREATE TABLE name_05 (id name);
insert into name_05 values ('');
select * from name_05;
drop table name_05;