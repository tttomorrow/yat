-- @testpoint: 在触发器中给临时表插入数据，合理报错
-- @modify at: 2020-11-24
--建表
drop table if exists temp_table_065;
drop table if exists temp_table_065_bak;
create temporary table temp_table_065(id int,name varchar2(10),sal number);
create temporary table temp_table_065_bak(id int,name varchar2(10),sal number);
--创建触发器函数
CREATE OR REPLACE FUNCTION tri_insert_func() RETURNS TRIGGER AS
           $$
           DECLARE
           BEGIN
                   INSERT INTO temp_table_065 VALUES(NEW.id, NEW.name, NEW.sal);
                   RETURN NEW;
           END
           $$ LANGUAGE PLPGSQL;
/
--创建触发器，报错
DROP TRIGGER if exists temporary_trigger on temp_table_065_bak;
CREATE TRIGGER temporary_trigger
           BEFORE INSERT ON temp_table_065_bak
           FOR EACH ROW
           EXECUTE PROCEDURE tri_insert_func();
/

--插入数据
insert into temp_table_065 values(1,'aaa',2600);
insert into temp_table_065 values(2,'bbb',2600);
insert into temp_table_065 values(3,'ccc',2800);
--查询
select * from temp_table_065;
--删除函数
DROP FUNCTION tri_insert_func();
--删表
drop table temp_table_065;
drop table temp_table_065_bak;