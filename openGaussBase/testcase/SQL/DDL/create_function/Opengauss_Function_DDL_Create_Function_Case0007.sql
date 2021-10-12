--  @testpoint:创建同名不同参的函数，合理报错
drop function if exists func_increment_plsql(i integer);
CREATE OR REPLACE FUNCTION func_increment_plsql(i integer) RETURNS integer AS $$
        BEGIN
                RETURN i + 1;
        END;
$$ LANGUAGE plpgsql;
/
select proname from pg_proc where proname='func_increment_plsql';

---创建同名不同参的函数,合理报错
CREATE OR REPLACE FUNCTION func_increment_plsql(j integer) RETURNS integer AS $$
        BEGIN
                RETURN j + 1;
        END;
$$ LANGUAGE plpgsql;
/
drop function func_increment_plsql(i integer);