--  @testpoint:创建函数和表结合，使用RETURNS TABLE 子句
--建表
DROP TABLE IF EXISTS sales2;
create table sales2(itemno integer,quantity integer,price numeric);
insert into sales2 values (100,15,11.2),(101,22,12.3);

--创建函数，使用RETURNS TABLE子句
DROP FUNCTION if EXISTS extended_sales2(p_itemno IN integer);
CREATE FUNCTION extended_sales2(p_itemno IN integer)RETURNS TABLE(quantity integer, total numeric) AS $$
BEGIN
RETURN QUERY SELECT sales2.quantity, sales2.quantity * sales2.price FROM sales2
WHERE itemno = p_itemno;
END;
$$ LANGUAGE plpgsql;
/
call extended_sales2(101);

drop table sales2;
drop FUNCTION extended_sales2;