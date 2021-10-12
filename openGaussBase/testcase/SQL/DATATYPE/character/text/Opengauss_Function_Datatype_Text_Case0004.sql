-- @testpoint: 插入空值
-- @modified at: 2020-11-16

drop table if exists test_text_04;
create table test_text_04(id int,c_text text,c_t text);
insert into test_text_04 values(1,'','aaa');
insert into test_text_04 values(1,'bbb',null);
select * from test_text_04;
drop table test_text_04;