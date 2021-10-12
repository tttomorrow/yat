create table xaxb
(
    id int,
    name char(23)
);

insert into xaxb values(0, '111'),(1, '33333'),(3,'555555');
commit;

declare
c int;
begin
    c := DBMS_STATS.auto_sample_size;
    dbms_output.put_line('DBMS_STATS.AUTO_SAMPLE_SIZE'||'is'||c);
end;
/

create or replace procedure test_procedure()
as
    ok int;
begin
    ok := 12;
end;
/

call test_procedure();

drop procedure test_procedure;

CREATE PROCEDURE P1 IS A CHAR(100) ;
 TYPE CURTY IS REF CURSOR ;
 CURSOR1 SYS_REFCURSOR;
 CURSOR2 CURTY ;
 BEGIN
 OPEN CURSOR2 FOR SELECT C_CHAR , IF(EXISTS(SELECT C_CHAR FROM ZSHARDING_TBL_P1 B WHERE C.C_CHAR<B.C_VARCHAR), 'condition is true', 'condition is false') AS IFCOL FROM ZSHARDING_TBL_P1 C WHERE C_VARCHAR LIKE '%c%%' ESCAPE 'c' OR C_VARCHAR2 LIKE '%c%%' ESCAPE 'c' ORDER BY C_CHAR , C_VARCHAR , C_VARCHAR2 , C_INT , C_INTEGER , C_BIGINT , C_DECIMAL , C_NUMBER , C_NUMERIC , C_BOOL , C_BOOLEAN , C_TIMESTAMP, C_DATE, C_DATETIME,C_FLOAT ;
 CURSOR1 := CURSOR2 ;
 DBMS_SQL.RETURN_RESULT(CURSOR1);
 END P1;
 /
 EXECUTE P1 ;
 DROP PROCEDURE IF EXISTS P1;