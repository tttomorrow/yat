-- @testpoint: 创建行存表，插入正常值
-- @modified at: 2020-11-13

drop table if exists name_01;
CREATE  TABLE name_01 (id name) WITH (orientation=row);
insert into name_01 values ('test');
select * from name_01;
drop table name_01;