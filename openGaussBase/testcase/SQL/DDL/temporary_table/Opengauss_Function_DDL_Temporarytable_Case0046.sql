-- @testpoint: 创建临时表，字段名超过63位
-- @modify at: 2020-11-24
--建表，字段名超过63位，截取前63位
drop table if exists temp_table_046;
create  temporary table temp_table_046(qwertyuiopqasdfghjklzxcvbnmpolkijuyhtgfrdppoiuytrqwelkijhgfdmnbqwewr int);
--插入数据（字段名超过63位，截取）
insert into temp_table_046(qwertyuiopqasdfghjklzxcvbnmpolkijuyhtgfrdppoiuytrqwelkijhgfdmnbqwewr) values(generate_series(1,100));
--查询
select count(*) from temp_table_046;
--插入数据，使用63位字段名
insert into temp_table_046(qwertyuiopqasdfghjklzxcvbnmpolkijuyhtgfrdppoiuytrqwelkijhgfdmnb)values(generate_series(101,110));
--查询
select count(*) from temp_table_046;
--删表
drop table temp_table_046;