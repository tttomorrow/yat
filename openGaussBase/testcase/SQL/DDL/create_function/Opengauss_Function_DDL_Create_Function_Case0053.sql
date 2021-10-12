--  @testpoint:OUT模式的参数用在RETURNS TABLE的函数定义中，合理报错
--创建表
DROP TABLE IF EXISTS sales;
create table sales(itemno integer,quantity integer,price numeric);
insert into sales values (100,15,11.2),(101,22,12.3);

--创建函数，指定OUT参数模式
DROP FUNCTION if EXISTS extended_sales(p_itemno OUT integer);
CREATE FUNCTION extended_sales(p_itemno OUT integer)RETURNS TABLE(quantity integer, total numeric) AS $$
BEGIN
RETURN QUERY SELECT quantity, quantity * price FROM sales
WHERE itemno = p_itemno;
END;
$$ LANGUAGE plpgsql;
/
drop table sales;