-- @testpoint: 表与自定义函数
drop table if exists t1;
CREATE TABLE t1(a int);
INSERT INTO t1 VALUES(1),(10);
CREATE OR REPLACE FUNCTION fun_for_return_query() RETURNS SETOF t1 AS $$
DECLARE
   r t1%ROWTYPE;
BEGIN
   RETURN QUERY select * from t1;
END;
$$ language plpgsql;
/
call fun_for_return_query();
DROP FUNCTION if exists fun_for_return_query();
drop table if exists t1 CASCADE;