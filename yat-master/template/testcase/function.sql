create or replace function test_function() return int
as
    ok int;
begin
    ok := 12;
    return ok;
end;
/

select test_function();

drop function test_function;