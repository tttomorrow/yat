-- @testpoint: mod函数用于存储过程
drop PROCEDURE if exists mod_procedure_test;
CREATE OR REPLACE PROCEDURE mod_procedure_test
is
mod_procedure_test bigint;
begin
mod_procedure_test:= 6552154111;
raise info':%',(mod(mod_procedure_test,32)+mod(mod_procedure_test,3255241));
end;
/
call mod_procedure_test();
drop PROCEDURE if exists mod_procedure_test;
