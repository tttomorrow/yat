-- @testpoint: 插入null值

drop table if exists name_06;
CREATE TABLE name_06 (id name);
insert into name_06 values (null);
select * from name_06;
drop table name_06;