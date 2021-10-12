-- @testpoint: 插入非法字符,合理报错

drop table if exists name_09;
CREATE TABLE name_09 (id name);
insert into name_09 values (%%%%%);
select * from name_09;
drop table name_09;