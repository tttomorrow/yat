--  @testpoint:创建复合类型，并且在一个函数定义中使用它
--创建复合类型
drop type if exists complex cascade;
create type complex as(r double precision, i double precision);
--创建复合类型
drop type if exists inventory_item;
create type inventory_item as(name text,number int,price numeric);
--建表
drop table if exists on_hand;
create table on_hand( item inventory_item, count integer);
--插入数据
insert into on_hand values (('fuzzy dice',42,1.99),1000);
--创建函数
drop function if exists price_extension;
create function price_extension(inventory_item,integer) returns numeric as 'select $1.price * $2' language sql;
/
--调用函数
 select price_extension(item,10) from on_hand;
--删除复合类型complex
drop type if exists complex;
--删除复合类型inventory_item，不加cascade，合理报错
drop type if exists inventory_item;
--删除复合类型inventory_item，添加cascade，删除成功
drop type if exists inventory_item cascade;
--删除表
drop table on_hand;
--删除函数
drop function if exists price_extension;