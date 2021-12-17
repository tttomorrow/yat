-- @testpoint: 表和视图
drop table if exists table_1;
create table table_1(id int,sname char(20),city varchar(20),number number);
insert into table_1 values(1,'joe','a',12323455646);
insert into table_1 values(2,'jojo','b',124232345456);
insert into table_1 values(3,'jane','c',12557676878);
CREATE VIEW table_1_View AS SELECT * FROM table_1 WHERE sname like 'j%';
SELECT * FROM table_1_View;
DROP VIEW table_1_View;
CREATE VIEW table_2_View AS SELECT * FROM table_1 WHERE id =1;
SELECT * FROM table_2_View;
DROP VIEW table_2_View;
CREATE VIEW table_3_View AS SELECT * FROM table_1;
SELECT * FROM table_3_View;
DROP VIEW table_3_View;
drop table if exists table_1;