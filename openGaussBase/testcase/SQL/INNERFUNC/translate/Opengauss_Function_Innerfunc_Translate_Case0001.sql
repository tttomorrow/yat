-- @testpoint: 字符处理函数translate，入参类型覆盖char/varchar;
-- select translate(lpad('abc',80,'abc'),'cba','在西安');

select translate('abcabc'::varchar(6),'cba','abc');
select translate('abcabc'::char(60),'cba','abc');
select translate('abcabc'::char(60),'cba ','abcc');

