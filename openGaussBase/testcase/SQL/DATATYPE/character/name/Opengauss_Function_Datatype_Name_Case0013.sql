-- @testpoint: 创建本地临时行存表，字段类型设为name


drop table if exists name_13;
CREATE TEMPORARY TABLE name_13 (id name) WITH (orientation=row, compression=no);
insert into name_13 values ('test');
select * from name_13;
drop table name_13;