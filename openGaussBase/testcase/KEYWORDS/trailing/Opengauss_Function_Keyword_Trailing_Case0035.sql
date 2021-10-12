--  @testpoint:opengauss关键字trailing(保留)，结合函数使用验证功能正常

select trim(trailing 'x' from 'xxABCDxx') as result;
select trim(trailing 'x' from 'ABCDxx') as result;
select trim(trailing 'x' from 'xxABCD') as result;
select trim(trailing 'x' from 'ABxxCD') as result;
select trim(trailing 'x' from 'ABCD') as result;
