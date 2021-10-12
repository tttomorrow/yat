-- @testpoint: 创建临时表，并指定字段的缺省值
-- @modify at: 2020-11-24
--建表
drop table if exists temp_table_048;
create  temporary table temp_table_048(a int,b char(20) DEFAULT 'opengauss',c number);
--插入数据
insert into temp_table_048(a,c) values(1,585.28);
insert into temp_table_048 values(1,'测试',585.28);
--查询表（第一条数据b字段使用默认值，第二条数据b字段使用新插入的值)
select * from temp_table_048;
--删表
drop table temp_table_048;


