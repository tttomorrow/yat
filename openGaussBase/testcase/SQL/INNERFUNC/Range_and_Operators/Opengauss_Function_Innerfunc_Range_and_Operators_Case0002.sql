-- @testpoint: numrange(numeric, numeric, [text]) 描述：表示一个范围,入参为其他类型时，合理报错

select numrange(1.1,'a','[]') as result;
select numrange('abc','111','[]') as result;
select numrange(2.3,111.5,'1') as result;
