-- @testpoint: 函数basicemailmasking，对出现第一个'@'之前的email文本进行脱敏

--@之前是英文
select basicemailmasking('abcd@gmail.com') as result;
--@之前是数字
select basicemailmasking('1122356@gmail.com') as result;
--@之前为中文
select basicemailmasking('你好@gmail.com') as result;
--@之前为特殊字符
select basicemailmasking('#￥%&&*@gmail.com') as result;
--当文本中含有两个@时
select basicemailmasking('#￥%&&*@gmail.@com') as result;
--当文本中不含@符号时
select basicemailmasking('abcdgmail.com') as result;
--参数为变量
drop table if exists test_01;
create table test_01 (col1 varchar2(20),col2 integer,col3 varchar2(20));
insert into test_01 values('你好@qaz.com', 10, 'abc');
select basicemailmasking(col1)from test_01;
drop table if exists test_01;