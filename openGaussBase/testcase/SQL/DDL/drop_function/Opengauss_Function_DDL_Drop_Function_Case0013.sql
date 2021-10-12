--  @testpoint:添加cascade参数，删除函数，函数体返回依赖表
--建表
DROP TABLE IF EXISTS sales3;
create table sales3(itemno integer,quantity integer,price numeric);
insert into sales3 values (100,15,11.2),(101,22,12.3);
select * from sales3;

--创建函数，使用RETURNS TABLE子句
DROP FUNCTION if EXISTS extended_sales3(p_itemno IN integer);
CREATE FUNCTION extended_sales3(p_itemno IN integer)RETURNS TABLE(quantity integer, total numeric) AS $$
BEGIN
RETURN QUERY SELECT sales3.quantity, sales3.quantity * sales3.price FROM sales3
WHERE itemno = p_itemno;
END;
$$ LANGUAGE plpgsql;
/
call extended_sales3(101);


drop FUNCTION extended_sales3(p_itemno IN integer) cascade;
drop table sales3;