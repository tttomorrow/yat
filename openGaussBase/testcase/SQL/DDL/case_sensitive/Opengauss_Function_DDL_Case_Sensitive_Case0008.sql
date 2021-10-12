--  @testpoint: --验证group by 中字段的大小写
select * from false_1;
select sum(a),b from false_1 group by b order by 1,2;
select sum(a),b from false_1 group by B;