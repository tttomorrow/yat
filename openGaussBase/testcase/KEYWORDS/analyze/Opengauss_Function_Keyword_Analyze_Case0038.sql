--  @testpoint:使用ANALYZE语句更新统计信息


drop table if exists customer_info;
CREATE TABLE customer_info
(
WR_RETURNED_DATE_SK       INTEGER                       ,
WR_RETURNED_TIME_SK       INTEGER                       ,
WR_ITEM_SK                INTEGER               NOT NULL,
WR_REFUNDED_CUSTOMER_SK   INTEGER
)
;

ANALYZE customer_info;
drop table customer_info;