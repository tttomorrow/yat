-- @testpoint: 创建表与触发器交互
drop table if exists table_001;
drop table if exists table_002;
create table table_001(id int,name varchar2(10),sal number);
create table table_002(id int,name varchar2(10),sal number);
--创建触发器函数
CREATE OR REPLACE FUNCTION tri_insert_func() RETURNS TRIGGER AS
           $$
           DECLARE
           BEGIN
                   INSERT INTO table_001 VALUES(NEW.id, NEW.name, NEW.sal);
                   RETURN NEW;
           END
           $$ LANGUAGE PLPGSQL;
/
--创建触发器
CREATE TRIGGER table_trigger
           BEFORE INSERT ON table_002
           FOR EACH ROW
           EXECUTE PROCEDURE tri_insert_func();
/
--插入数据，调用触发器
insert into table_002 values(1,'aaa',2600);
insert into table_002 values(2,'bbb',2600);
insert into table_002 values(3,'ccc',2800);
select * from table_002;
select * from table_001;
DROP TRIGGER table_trigger ON table_002;
DROP FUNCTION tri_insert_func()CASCADE;
drop table if exists table_001;
drop table if exists table_002;