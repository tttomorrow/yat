-- @testpoint:存储过程非动态语句查询语句

drop table if exists sections_t3;
CREATE TABLE sections_t3
(
   section       NUMBER(4) ,
   section_name  VARCHAR2(30),
   manager_id    NUMBER(6),
   place_id      NUMBER(4)
);

 DECLARE
   section       NUMBER(4) := 280;
   section_name  VARCHAR2(30) := 'Info support';
   manager_id    NUMBER(6) := 103;
   place_id      NUMBER(4) := 1400;
   new_colname   VARCHAR2(10) := 'sec_name';
BEGIN
    EXECUTE IMMEDIATE 'insert into sections_t3 values(:1, :2, :3, :4)'
       USING section, section_name, manager_id,place_id;

    EXECUTE IMMEDIATE 'alter table sections_t3 rename section_name to ' || new_colname;
END;
/

SELECT * FROM sections_t3;
DROP TABLE sections_t3;

