-- @testpoint: 窗口函数列存表支持情况

--创建列存表
create table goods_sale_table ( goods_id int, goods_type varchar ( 1000 ), goods_sale int )  WITH (ORIENTATION = COLUMN);
insert into goods_sale_table
values
	( 1, '电脑数码', 400 ),
	( 2, '家用电器', 600 ),
	( 3, '电脑数码', 500 ),
	( 4, '游戏', 550 ),
	( 5, '家用电器', 1000 ),
	( 6, '电脑数码', 1200 ),
	( 7, '游戏', 700 ),
	( 8, '游戏', 750 ),
	( 9, '家用电器', 1100 ),
	( 10, '电脑数码', 900 ),
	( 11, '电脑数码', 900 );

--列存表对不同函数的支持情况
--窗口函数 row_number ()支持
select goods_id, goods_type, row_number ( ) over ( partition by goods_type order by goods_sale desc ) from goods_sale_table;

--窗口函数 rank()，支持
select goods_id, goods_type, rank ( ) over ( partition by goods_type order by goods_sale desc ) from goods_sale_table;

--窗口函数 DENSE_RANK()
select goods_id, goods_type, DENSE_RANK ( ) over ( partition by goods_type order by goods_sale desc ) from goods_sale_table;

--窗口函数CUME_DIST()
select goods_id, goods_type, cume_dist ( ) over ( partition by goods_type order by goods_sale desc ) from goods_sale_table;

--窗口函数percent_rank( )，支持
select goods_id, goods_type, percent_rank ( ) over ( partition by goods_type order by goods_sale desc ) from goods_sale_table;

--窗口函数NTILE(num_buckets integer)，支持
select goods_id, goods_type, NTILE(3) over ( partition by goods_type order by goods_sale desc ) from goods_sale_table;

--窗口函数LAG(value any [, offset integer [, default any ]])
select goods_id, goods_type, lag (goods_id,2) over ( partition by goods_type order by goods_type desc ) from goods_sale_table;

--窗口函数LEAD(value any [, offset integer [, default any ]])
select goods_id, goods_type, lead(goods_id,2) over ( partition by goods_type order by goods_type desc ) from goods_sale_table;

--窗口函数FIRST_VALUE(value any)
select goods_id, goods_type, first_value(goods_sale) over ( partition by goods_type order by goods_type desc ) from goods_sale_table;

--窗口函数LAST_VALUE(value any)
select goods_id, goods_type, first_value(3) over ( partition by goods_type order by goods_type desc ) from goods_sale_table;

--窗口函数NTH_VALUE(value any, nth integer)
select goods_id, goods_type, nth_value(goods_id,1) over ( partition by goods_type order by goods_sale desc ) from goods_sale_table;

--清理环境
drop  table goods_sale_table;