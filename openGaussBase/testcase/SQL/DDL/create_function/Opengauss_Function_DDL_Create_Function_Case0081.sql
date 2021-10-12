drop FUNCTION if EXISTS x_testfun1;
CREATE FUNCTION x_testfun1 (c_int int DEFAULT 2020 and 2019)  RETURNS int  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql;
/
call x_testfun1();
drop FUNCTION x_testfun1;