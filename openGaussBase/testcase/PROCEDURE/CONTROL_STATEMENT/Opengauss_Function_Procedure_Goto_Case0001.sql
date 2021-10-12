-- @testpoint: 存储过程中goto语句使用

create or replace procedure goto_test()
as
declare
    v1  int;
begin
    v1  := 0;
        loop
        exit when v1 > 100;
                v1 := v1 + 2;
                if v1 > 25 then
                        goto pos1;
                end if;
        end loop;
	<<pos1>>
	v1 := v1 + 10;
	raise info 'v1 is %. ', v1;
end;
/
call goto_test();
drop procedure goto_test;


