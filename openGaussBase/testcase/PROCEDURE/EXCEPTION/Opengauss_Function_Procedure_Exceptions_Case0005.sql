-- @testpoint: 预定义异常CASE_NOT_FOUND，捕获输出错误码和错误信息

drop table if exists TB_USER_1;
CREATE TABLE TB_USER_1
(
    ID INTEGER NOT NULL,
    USER_NAME VARCHAR2(20) NOT NULL,
    USER_AGE INTEGER NOT NULL
);
insert into TB_USER_1(ID,USER_NAME,USER_AGE)values(20,'zz',80);

declare
V_AGE TB_USER_1.USER_AGE%TYPE;
V_NAME TB_USER_1.USER_NAME%TYPE;
BEGIN
  SELECT USER_NAME, USER_AGE INTO V_NAME, V_AGE FROM TB_USER_1 WHERE ID=20;
     raise info ',%',V_NAME;
     raise info ',%',V_AGE;
  CASE
    WHEN V_AGE < 18 THEN
      raise info 'is a child%',V_NAME;
    WHEN V_AGE < 50 THEN
      raise info 'is not a child%',V_NAME;
  END CASE;
  EXCEPTION
    WHEN CASE_NOT_FOUND THEN
      raise info 'ERROR MSG:%',SQLERRM;
END;
/
drop table TB_USER_1;