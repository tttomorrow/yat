-- @testpoint: to_clob函数返回值用于算术运算

select to_clob(to_char('11111')+to_char('22'));
select to_clob(1)+to_clob(2);