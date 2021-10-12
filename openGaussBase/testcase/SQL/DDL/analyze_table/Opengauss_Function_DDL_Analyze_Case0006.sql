-- @testpoint: 收集分区表的统计信息。
drop table if exists customer_par;
create table customer_par
(
wr_returned_date_sk       integer                       ,
wr_returned_time_sk       integer                       ,
wr_item_sk                integer               not null,
wr_refunded_customer_sk   integer
)
partition by range(wr_returned_date_sk)
(
partition p1 values less than(2452275),
partition p2 values less than(2452640),
partition p3 values less than(2453000),
partition p4 values less than(maxvalue)
)
enable row movement;
insert into customer_par values(2452260,11,111,1111);
insert into customer_par values(2452530,22,222,2222);
insert into customer_par values(2452700,33,333,3333);
analyze customer_par;
select * from pg_statistic where starelid = (select oid from pg_class where relname = 'customer_par');
drop table if exists customer_par;