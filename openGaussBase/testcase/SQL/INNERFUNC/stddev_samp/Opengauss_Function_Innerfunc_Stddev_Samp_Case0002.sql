-- @testpoint: 入参为字符类型的列，分组求标准差,合理报错
drop table if exists test1;
create table test1(col_1 char, col_2 nchar(100), col_3 varchar(100), col_4 varchar2(100), col_5 nvarchar2(100), col_6 text, col_7 clob);
insert into test1 values('i','ready','wait for a moment','doctor actor lawyer or a singer','why not president be a dreamer','you can be just the one u wanna be','policeman firefighter or a postman');
insert into test1 values('u','o','moment!','doctor','be a dreamer!','u wanna be!','why not be like your old man!');
select stddev_samp(col_1), stddev_samp(col_2), stddev_samp(col_3), stddev_samp(col_4), stddev_samp(col_5), stddev_samp(col_6), stddev_samp(col_7) from test1;
drop table if exists test1;