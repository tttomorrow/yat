-- @testpoint: 输出CASE_NOT_FOUND异常（一般case语句，不捕捉异常，合理报错;捕捉异常，执行成功。）

drop table if exists CASE_TEST;
CREATE TABLE CASE_TEST
(
    ID INTEGER NOT NULL,
    NAME VARCHAR2(20) NOT NULL,
    job INTEGER NOT NULL
);
insert into CASE_TEST(ID,NAME,job)values(20,'zz',1);
insert into CASE_TEST(ID,NAME,job)values(30,'zz',2);
insert into CASE_TEST(ID,NAME,job)values(40,'zz',3);

create or replace procedure test_case_procedure(str boolean)  as
v_sex CASE_TEST.job%TYPE;
begin
   select job into v_sex from CASE_TEST where ID=40;
   case v_sex
   when '1' then
    raise info 'teacher';
   when '2' then
      raise info 'IT';
   end case;
end;
/
call test_case_procedure(true);

create or replace procedure test_case_procedure(str boolean)  as
v_sex CASE_TEST.job%TYPE;
begin
   select job into v_sex from CASE_TEST where ID=40;
   case v_sex
   when '1' then
    raise info 'teacher';
   when '2' then
    raise info 'IT';
   end case;
 EXCEPTION
    WHEN CASE_NOT_FOUND THEN
     raise info 'case not found';
    WHEN OTHERS THEN
     raise info 'ERROR CODE:%',SQLCODE,'ERROR CODE:%',CHR(10),'ERROR MSG:%',SQLERRM;
END;
/
call test_case_procedure(true);
drop procedure test_case_procedure;
drop table CASE_TEST;