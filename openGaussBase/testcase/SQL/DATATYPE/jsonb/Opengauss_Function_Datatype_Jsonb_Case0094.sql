-- @testpoint: jsonb额外支持操作函数：jsonb_hash(遍历json结构和数据，计算出来一个hash值),不合理入参，合理报错

--合理入参
select jsonb_hash('"abcdefg"');
select jsonb_hash('true');
select jsonb_hash('null');
select jsonb_hash('100.6');
select jsonb_hash('-100.99');
select jsonb_hash('{"false":0}');
select jsonb_hash('[{"false":0},100,null,true,"qwert"]');

--不合理入参
select jsonb_hash('abcdefg');
select jsonb_hash('123','-852.36','235.6');
select jsonb_hash('abcdefg,qwee,qaz');
select jsonb_hash('[{"false":0},100,null,true,qwert]');