-- @testpoint: 查询临时表数据，与聚合函数min结合使用
-- @modify at: 2020-11-24
--建表
drop table if exists temp_table_071;
create TEMPORARY table temp_table_071 (id int,name char(20),class char(10),course char(20),score float(1));
--插入数据
insert into temp_table_071 values(4,'小明',1,'数学',87.5);
insert into temp_table_071 values(2,'小红',2,'数学',62);
insert into temp_table_071 values(1,'小蓝',1,'数学',77.5);
insert into temp_table_071 values(2,'小黑',1,'数学',97.5);
insert into temp_table_071 values(3,'小黄',2,'数学',88);
insert into temp_table_071 values(5,'小紫',1,'数学',57);
insert into temp_table_071 values(7,'小白',1,'数学',100);
--查询
SELECT min(score) FROM temp_table_071 where class = 2 and course = '数学';
--删表
drop table if exists temp_table_071;