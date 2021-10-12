--  @testpoint:opengauss关键字NEXT(非保留)，使用RETURN NEXT向结果集中追加结果
drop table if exists t1;
CREATE TABLE t1(a int);
INSERT INTO t1 VALUES(1),(10);
CREATE OR REPLACE FUNCTION fun_for_return_next() RETURNS SETOF t1 AS $$
DECLARE
   r t1%ROWTYPE;
BEGIN
   FOR r IN select * from t1
   LOOP
      RETURN NEXT r;
   END LOOP;
   RETURN;
END;
$$ LANGUAGE PLPGSQL;
/
call fun_for_return_next();
drop FUNCTION fun_for_return_next;
drop table t1;
