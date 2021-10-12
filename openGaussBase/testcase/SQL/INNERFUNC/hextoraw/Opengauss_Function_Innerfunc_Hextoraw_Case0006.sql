-- @testpoint: hextoraw函数和rawtohex结合使用
select hextoraw(rawtohex('125abc578')) from sys_dummy;
select rawtohex(hextoraw(rawtohex('125abc578'))) from sys_dummy;