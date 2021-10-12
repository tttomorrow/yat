-- @testpoint:存储过程非动态语句查询语句

drop table if exists sections_t2;
CREATE TABLE sections_t2
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
    EXECUTE IMMEDIATE 'insert into sections_t2 values(:1, :2, :3, :1)'
       USING section, section_name, manager_id;
    EXECUTE IMMEDIATE 'insert into sections_t2 values(:4, :2, :1, :1)'
       USING section, section_name, manager_id;
END;
/

SELECT * FROM sections_t2;
DROP TABLE sections_t2;









