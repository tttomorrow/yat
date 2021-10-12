-- @testpoint: 插入非法字符，合理报错

drop table if exists dec_09;
CREATE  TABLE dec_09 (id DEC(4,2));
insert into dec_09 values ('……（*');
drop table dec_09;