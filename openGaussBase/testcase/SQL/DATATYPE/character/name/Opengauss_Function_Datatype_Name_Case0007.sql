-- @testpoint: 插入其他类型

drop table if exists name_07;
CREATE TABLE name_07 (id name);
insert into name_07 values ('test');
insert into name_07 values (10000);
insert into name_07 values (100.999);
insert into name_07 values (date'2020-02-02');
insert into name_07 values (TRUE);
insert into name_07 values (HEXTORAW('DEADBEEF'));
select * from name_07;
drop table name_07;