drop function if exists d_test1("arg_test1*#" integer, "arg_test2*#" integer);
CREATE FUNCTION d_test1("arg_test1*#" integer, "arg_test2*#" integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
/
select  proargnames from pg_proc where proname='d_test1';
call d_test1(-9,-8);
drop FUNCTION d_test1;