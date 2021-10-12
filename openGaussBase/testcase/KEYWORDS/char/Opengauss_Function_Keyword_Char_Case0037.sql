-- @testpoint: 指定字符串长度，不足补空格
drop table if exists char_type_t1;
CREATE TABLE char_type_t1(CT_COL1 CHAR(5));
insert into char_type_t1 (CT_COL1) values('hi');
drop table if exists char_type_t1;