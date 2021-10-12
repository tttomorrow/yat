drop FUNCTION if EXISTS u_testfun1(c_int int);
CREATE FUNCTION u_testfun1 (c_int int) RETURNS int  AS $$
        BEGIN
                RETURN (c_int);
        END;
$$ LANGUAGE plpgsql
fenced ;
/


