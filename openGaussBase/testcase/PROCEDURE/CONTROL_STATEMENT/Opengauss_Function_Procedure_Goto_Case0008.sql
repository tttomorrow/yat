-- @testpoint: 存储过程中使用goto语句，goto跳转到loop语句，不支持 合理报错

create or replace procedure goto_test()
as
declare
    v1  int;
begin
    v1  := 0;
        goto qqq;
        loop
        <<qqq>>
        exit when v1 > 100;
                v1 := v1 + 2;
                if v1 > 25 then

                end if;
        end loop;
	v1 := v1 + 10;
	raise info 'v1 is %. ', v1;
end;
/
call goto_test();
drop procedure goto_test;
