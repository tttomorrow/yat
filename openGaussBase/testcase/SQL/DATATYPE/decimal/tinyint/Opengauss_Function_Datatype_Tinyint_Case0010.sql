-- @testpoint: 插入字符串类型，合理报错

drop table if exists tinyint10;
create table tinyint10 (name tinyint);
insert into tinyint10 values ('123abc');
insert into tinyint10 values ('1a2');
insert into tinyint10 values ('abc123');
drop table tinyint10;