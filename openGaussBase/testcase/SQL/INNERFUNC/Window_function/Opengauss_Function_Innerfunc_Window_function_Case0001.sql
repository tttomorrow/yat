-- @testpoint: row_number() 描述：各组内值生成连续排序序号，其中，相同的值其序号也不相同

--现想了解每种产品类型销量前2名的商品,输出要求如下：goods_id 商品id (销量排名前2名) goods_type 商品种类
create table goods_sale_table ( goods_id int, goods_type varchar ( 1000 ), goods_sale int );
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

--执行步骤
select
	a.goods_id,
	a.goods_type
from
	( select goods_id, goods_type, row_number ( ) over ( partition by goods_type order by goods_sale desc ) from goods_sale_table ) a
where
	row_number <= 2;

--清理环境
drop table goods_sale_table;


