--  @testpoint:修改序列的最大值
--创建序列
drop SEQUENCE if exists b_serial;
CREATE SEQUENCE b_serial INCREMENT by 2 MAXVALUE 5;
--修改序列最大值
alter SEQUENCE b_serial MAXVALUE 7;
--调用函数nextval，四次，分别返回1,3,5,7
select nextval('b_serial');
select nextval('b_serial');
select nextval('b_serial');
select nextval('b_serial');
--第五次调用，合理报错
select nextval('b_serial');
--修改序列最大值为 NO MAXVALUE
alter SEQUENCE b_serial NO MAXVALUE;
--查询序列max_value（9223372036854775807）
select sequence_name,max_value from b_serial where sequence_name = 'b_serial';
--删除序列
drop SEQUENCE b_serial;




