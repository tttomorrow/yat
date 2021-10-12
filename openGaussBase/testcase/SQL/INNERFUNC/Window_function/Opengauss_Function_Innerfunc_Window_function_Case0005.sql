-- @testpoint: PERCENT_RANK() 为各组内对应值生成相对序号

create table goods_sale_table ( goods_id int, goods_type varchar ( 1000 ), goods_sale int );
insert into goods_sale_table
values
	( 1, '电脑数码', 400 ),
	( 2, '家用电器', 600 ),
	( 3, '电脑数码', 550 ),
	( 4, '游戏', 550 ),
	( 5, '家用电器', 1000 ),
	( 6, '电脑数码', 1200 ),
	( 7, '游戏', 700 ),
	( 8, '游戏', 750 ),
	( 9, '家用电器', 1100 ),
	( 10, '电脑数码', 900 ),
	( 11, '电脑数码', 900 );

select goods_id, goods_type, percent_rank ( ) over ( partition by goods_type order by goods_sale desc ) from goods_sale_table;

--清理环境
drop table goods_sale_table;