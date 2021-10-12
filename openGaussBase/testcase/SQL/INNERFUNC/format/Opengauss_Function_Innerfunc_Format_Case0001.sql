-- @testpoint: 格式化字符串:有效值
SELECT format('Hello %s, %1$s', 'World');
SELECT format('Hello %s, %1$s', 'Jim');
SELECT format('Hello %s, %1$s', '123');
SELECT format('Hello %s, %1$s', '世界');
SELECT format('Hello %s, %1$s', 'Jim，我今年8岁，I have a dream !');