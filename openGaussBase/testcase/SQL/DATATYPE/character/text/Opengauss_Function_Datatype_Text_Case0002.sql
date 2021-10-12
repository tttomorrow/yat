-- @testpoint: 创建表，插入正常范围值


drop table if exists test_text_02;
create table test_text_02(id int,c_text text);
insert into test_text_02 values(1,'abcqjigjlfdjpog2ow3-0r43eurt9eiuopfjdgjljgabcqjigjlfdjpog2ow3j');
insert into test_text_02 values(2,'abc');
insert into test_text_02 values(3,'中国');
insert into test_text_02 values(4,'123Gauss');
insert into test_text_02 values(5,'１２３４％＃');
select * from test_text_02;
drop table test_text_02;
