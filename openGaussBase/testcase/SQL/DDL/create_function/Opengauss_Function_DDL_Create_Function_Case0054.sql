--  @testpoint:INOUT模式的参数用在RETURNS TABLE的函数定义中，合理报错
--建表
DROP TABLE IF EXISTS sales1;
create table sales1(itemno integer,quantity integer,price numeric);
insert into sales1 values (100,15,11.2),(101,22,12.3);

--创建函数，定义参数模式是INOUT
DROP FUNCTION if EXISTS extended_sales1(p_itemno INOUT integer);
CREATE FUNCTION extended_sales1(p_itemno INOUT integer)RETURNS TABLE(quantity integer, total numeric) AS $$
BEGIN
RETURN QUERY SELECT quantity, quantity * price FROM sales1
WHERE itemno = p_itemno;
END;
$$ LANGUAGE plpgsql;
/
drop table sales1;